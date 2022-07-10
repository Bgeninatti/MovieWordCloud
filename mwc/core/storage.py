import abc

import dropbox
from io import BytesIO

import attr

from mwc.core.cfg import load_settings

settings = load_settings()


@attr.s
class BaseStorage(abc.ABC):
    namespace: str = attr.ib()

    def get(
        self,
        filename: str,
    ) -> BytesIO:
        ...

    def save(
        self,
        filename: str,
        storage_object: BytesIO,
    ) -> None:
        ...


@attr.s
class DropBoxStorage(BaseStorage):
    namespace: str = attr.ib()
    _client = dropbox.Dropbox(settings['DROPBOX_TOKEN'])

    def __attrs_post_init__(self):
        if not self._folder_exists(self.namespace):
            self._create_folder(self.namespace)

    def _folder_exists(self, namespace):
        expected_path = f'/{namespace.lower()}'
        matches = self._client.files_search_v2(namespace).matches
        folder_matches = [
            match for match in matches
            if isinstance(match.metadata.get_metadata(), dropbox.files.FolderMetadata) and
               match.metadata.get_metadata().path_lower == expected_path
        ]
        if not folder_matches:
            return False
        else:
            return True

    def _create_folder(self, namespace):
        return self._client.files_create_folder_v2(f'/{namespace}')

    def get(
        self,
        filename: str,
    ) -> BytesIO:
        _, content = self._client.files_download(f'/{self.namespace}/{filename}')
        return content

    def save(
        self,
        filename: str,
        content: BytesIO,
    ) -> None:
        destination = f'/{self.namespace}/{filename}'
        self._client.files_upload(content.read(), destination)


def get_storage(namespace):
    return DropBoxStorage(namespace)
