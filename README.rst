===========================
Munch Swift storage backend
===========================

This module contains Swift storage backends to be used with Munch.

*******
Install
*******

Todo.

*******************
SwiftPrivateStorage
*******************

This one is meant to be used as the default Django storage backend.
It merely wraps django-storage-swift by:

* providing an extra Django setting for the container name
* ensuring a blank URL is returned for the file (since container is private)
* forcing auto_overwrite of files

We prefer to use a different setting for the container name rather than upstream's SWIFT_CONTAINER_NAME so that we can cleanly configure multiple Swift backends.

-----
Usage
-----

::

    # Add the following in Django settings
    DEFAULT_FILE_STORAGE = 'munch_storage_swift.SwiftPrivateStorage'
    DEFAULT_SWIFT_CONTAINER_NAME = 'private'

    SWIFT_AUTH_URL = 'https://auth.cloud.ovh.net/v2.0'
    SWIFT_AUTH_VERSION = '2.0'
    SWIFT_USERNAME = 'username'
    SWIFT_KEY = 'XXXXXXXXXX'
    SWIFT_TENANT_NAME = 'tenant_name'
    SWIFT_TENANT_ID = 'tenant_id'


******************
SwiftUploadStorage
******************

This one will do all of most of the above, except returning a blank URL.
Instead, we will return a URL using the provided base_url, regardless of the URL computed by upstream.

-----
Usage
-----

::

    # Add the following in Django settings
    UPLOAD_STORE_BACKEND = 'munch_storage_swift.SwiftUploadStorage'
    UPLOAD_STORE_SWIFT_CONTAINER_NAME = 'upload'

    SWIFT_AUTH_URL = 'https://auth.cloud.ovh.net/v2.0'
    SWIFT_AUTH_VERSION = '2.0'
    SWIFT_USERNAME = 'username'
    SWIFT_KEY = 'XXXXXXXXXX'
    SWIFT_TENANT_NAME = 'tenant_name'
    SWIFT_TENANT_ID = 'tenant_id'
