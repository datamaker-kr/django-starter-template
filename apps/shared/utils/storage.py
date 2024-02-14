import json
from urllib.parse import parse_qs, urlparse

from .string import str_to_bool


class BaseStorageParser:
    BACKEND = None
    OPTION_CASTS = {}

    def __init__(self, url):
        self.url = urlparse(url)
        self.query_params = self.url_querystring_to_dict()

    def __call__(self):
        storage = {'BACKEND': self.BACKEND}
        options = self.get_options()
        if options:
            storage['OPTIONS'] = options
        return storage

    def url_querystring_to_dict(self):
        query_string = self.url.query

        query_dict = parse_qs(query_string)

        for key, value in query_dict.items():
            if len(value) == 1:
                query_dict[key] = value[0]

        return {
            key: self.OPTION_CASTS[key](value) if key in self.OPTION_CASTS else value
            for key, value in query_dict.items()
        }

    def get_options(self):
        return None


class FileSystemStorageParser(BaseStorageParser):
    BACKEND = 'django.core.files.storage.FileSystemStorage'

    def get_options(self):
        options = {**self.query_params}

        location = ''
        if self.url.hostname:
            location = self.url.hostname
        if self.url.path:
            location += self.url.path

        if location:
            options['location'] = location
        return options


class StaticFilesStorageParser(FileSystemStorageParser):
    BACKEND = 'django.contrib.staticfiles.storage.StaticFilesStorage'


class S3StorageParser(BaseStorageParser):
    BACKEND = 'storages.backends.s3boto3.S3Boto3Storage'
    OPTION_CASTS = {
        'object_parameters': json.loads,
        'querystring_auth': str_to_bool,
        'max_memory_size': int,
        'querystring_expire': int,
        'file_overwrite': str_to_bool,
        'gzip': str_to_bool,
        'use_ssl': str_to_bool,
        'verify': str_to_bool,
        'proxies': json.loads,
        'transfer_config': json.loads,
    }

    def get_options(self):
        endpoint_url = '.'.join(self.url.hostname.split('.')[1:])
        return {
            'endpoint_url': f'https://{endpoint_url}',
            'bucket_name': self.url.path[1:],
            'access_key': self.url.username,
            'secret_key': self.url.password,
            'region_name': self.url.hostname.split('.')[0],
            **self.query_params,
        }


STORAGE_PARSERS = {
    'filesystem': FileSystemStorageParser,
    'staticfiles': StaticFilesStorageParser,
    's3': S3StorageParser,
}


def get_storages(env, storages=None):
    if storages is None:
        storages = ['default', ('staticfiles', 'staticfiles://')]

    storage_settings = {}

    for storage in storages:
        if isinstance(storage, tuple):
            storage_url = env(f'STORAGE_{storage[0].upper()}', default=storage[1])
            storage_name = storage[0]
        else:
            storage_url = env(f'STORAGE_{storage.upper()}')
            storage_name = storage

        storage_scheme = urlparse(storage_url).scheme
        parser_class = STORAGE_PARSERS[storage_scheme]
        storage_settings[storage_name] = parser_class(storage_url)()

    return storage_settings
