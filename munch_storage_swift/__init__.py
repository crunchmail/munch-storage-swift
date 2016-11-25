import hashlib
import string
import magic
from urllib.parse import urljoin

from swift.storage import swiftclient
from swift.storage import SwiftStorage as BaseSwiftStorage
from swiftclient.exceptions import ClientException
from django.conf import settings
from django.utils.deconstruct import deconstructible

__version__ = '0.1.0'
default_app_config = 'munch_storage_swift.apps.StorageApp'


class SwiftStorageException(Exception):
    def __init__(self, e):
        """
        @param e : the underlying exception
        """
        self.sub_e = e

    def __str__(self):
        return str(self.sub_e)


@deconstructible
class SwiftStorage(BaseSwiftStorage):
    def get_valid_name(self, name):
        # heavy sanitization of the filename,
        # it helps with manual management in swift
        s = name.strip().replace(' ', '_')
        valid_chars = "-_.():%s%s" % (string.ascii_letters, string.digits)
        return ''.join(c for c in s if c in valid_chars).strip()

    def _save(self, name, fd, headers=None):
        fd.seek(0)  # just to make sure
        content = fd.read()
        fd.seek(0)  # rewind to ensure we save the whole file

        file_sum = hashlib.md5(content).hexdigest()
        del content

        try:
            # saved = super()._save(name, fd, headers=headers)

            #######################################
            # TMP : wait for PR https://github.com/blacktorn/django-storage-swift/pull/56  # noqa
            # to be accepted and  for new release
            # In the meantime, we do our own save()
            content_type = magic.from_buffer(fd.read(1024), mime=True)
            # Go back to the beginning of the file
            fd.seek(0)
            swiftclient.put_object(
                self.storage_url,
                self.token,
                self.container_name,
                name,
                fd,
                http_conn=self.http_conn,
                content_type=content_type)

            saved = name
            ########################################

        except ClientException as e:
            raise SwiftStorageException(e)

        try:
            resp = swiftclient.head_object(
                self.storage_url, token=self.token,
                container=self.container_name, name=saved,
                http_conn=self.http_conn)
        except ClientException as e:
            raise SwiftStorageException(e)

        if resp.get('etag') != file_sum:
            raise SwiftStorageException('MD5 sum mismatch')
        return saved


class SwiftPrivateStorage(SwiftStorage):
    def __init__(self, *args, **kwargs):
        # Force empty name_prefix
        self.name_prefix = ''
        super().__init__(*args, **kwargs)
        # If we're saving a duplicate, overwrite the file.
        self.auto_overwrite = True

    def url(self, name):
        # Access by URL will not be allowed by Swift anyway, so don't bother
        return None


class SwiftUploadStorage(SwiftStorage):
    def __init__(self, base_url, *args, **kwargs):
        # Use specific container
        self.container_name = settings.UPLOAD_STORE['SWIFT_CONTAINER_NAME']
        # Force empty name_prefix
        self.name_prefix = ''
        super().__init__(*args, **kwargs)
        # Upstream needs to use its own base_url so don't touch it
        # but store our custom base_url for future use
        self._base_url = base_url
        # If we're saving a duplicate, overwrite the file.
        self.auto_overwrite = True

    def url(self, name):
        return urljoin(self._base_url, name)

    def _save(self, name, content):
        headers = None
        # if we're dealing with a file (not image),
        # set proper Content-Disposition header
        if content.kind == 'file':
            headers = {
                'Content-Disposition': 'attachment; filename="{}"'.format(
                    content.name)}

        return super()._save(name, content, headers=headers)
