from datetime import timedelta
from multicloud_storage.object import StorageObject
from typing import Iterator, List, Optional, Union
from io import BytesIO

from multicloud_storage.http import HttpMethod

from .client import StorageClient
from .log import logger


class Storage:
    """
    Storage.

    The Storage defines the interface for the "control" part of the two
    class hierarchies. It maintains a reference to an object of the
    Implementation hierarchy and delegates all of the real work to this object.
    """

    def __init__(self, client: StorageClient) -> None:
        self._client = client
        self._client.configure()

    def bucket_exists(self, name: str) -> bool:
        logger.debug("bucket_exists(name='%s')", name)
        return self._client.bucket_exists(name)

    def make_bucket(self, name: str) -> None:
        logger.debug("make_bucket(name='%s')", name)
        return self._client.make_bucket(name)

    def remove_bucket(self, name: str) -> None:
        logger.debug("remove_bucket(name='%s')", name)
        return self._client.remove_bucket(name)

    def put_object(
        self,
        bucket_name: str,
        name: str,
        data: BytesIO,
        size: int,
    ) -> None:
        logger.debug(
            "put_object(bucket_name='%s', name='%s', data=[omitted], size=%i)",
            bucket_name,
            name,
            size,
        )
        return self._client.put_object(bucket_name, name, data, size)

    def get_object(
        self,
        bucket_name: str,
        name: str,
    ) -> BytesIO:
        logger.debug(
            "get_object(bucket_name='%s',name='%s')", bucket_name, name
        )
        return self._client.get_object(bucket_name, name)

    def object_exists(self, bucket_name: str, name: str) -> bool:
        logger.debug(
            "object_exists(bucket_name='%s',name='%s')", bucket_name, name
        )
        return self._client.object_exists(bucket_name, name)

    def delete_object(self, bucket_name: str, name: str) -> None:
        logger.debug(
            "delete_object(bucket_name='%s',name='%s')", bucket_name, name
        )
        return self._client.delete_object(bucket_name, name)

    def get_presigned_url(
        self,
        bucket_name: str,
        name: str,
        method: Union[str, HttpMethod],
        expires: Optional[timedelta] = timedelta(days=1),
        content_type: Optional[str] = None,
        use_hostname: Optional[str] = None,
        secure: Optional[bool] = None,
    ) -> str:
        logger.debug(
            "get_presigned_url(bucket_name='%s',name='%s', method='%s',"
            " expires=%s, content_type='%s', use_hostname=%s, secure=%s)",
            bucket_name,
            name,
            method,
            expires,
            content_type,
            use_hostname,
            secure,
        )
        return self._client.get_presigned_url(
            bucket_name,
            name,
            method,
            expires,
            content_type,
            use_hostname,
            secure,
        )

    def list_objects(
        self,
        bucket_name: str,
        prefix: Optional[str] = None,
    ) -> Iterator[StorageObject]:
        logger.debug(
            "list_objects(bucket_name='%s',prefix='%s')",
            bucket_name,
            prefix,
        )
        return self._client.list_objects(bucket_name, prefix)

    def copy_object(
        self,
        source_bucket_name: str,
        source_name: str,
        destination_bucket_name: str,
        destination_name: str,
    ) -> None:
        logger.debug(
            "copy_object(source_bucket_name='%s',source_name='%s',"
            " destination_bucket_name='%s', destination_name='%s')",
            source_bucket_name,
            source_name,
            destination_bucket_name,
            destination_name,
        )
        self._client.copy_object(
            source_bucket_name,
            source_name,
            destination_bucket_name,
            destination_name,
        )

    def rename_object(
        self,
        bucket_name: str,
        name: str,
        new_name: str,
    ) -> None:
        logger.debug(
            "rename_object(bucket_name='%s', name='%s', new_name='%s')",
            bucket_name,
            name,
            new_name,
        )
        self._client.rename_object(
            bucket_name,
            name,
            new_name,
        )

    def concat_objects(
        self,
        bucket_name: str,
        destination_object: str,
        source_objects: List[str],
    ) -> None:
        logger.debug(
            "concat_objects(bucket_name='%s',"
            "destination_object='%s',source_objects=%s)",
            bucket_name,
            destination_object,
            source_objects,
        )
        return self._client.concat_objects(
            bucket_name, destination_object, source_objects
        )

    def md5_checksum(self, bucket_name: str, name: str) -> str:
        logger.debug("md5_hash(bucket_name='%s',name='%s')", bucket_name, name)
        return self._client.md5_checksum(bucket_name, name)
