import os
from typing import List

from hestia.paths import delete_path

from stores.exceptions import StoreNotFoundError


class BaseManager(object):
    KIND = None
    MODEL = None

    def validate_refs(self, refs: List[str]):
        if refs:
            store_names = self.MODEL.objects.filter(name__in=refs).values_list('name', flat=True)
            invalid_stores_refs = set(refs) - set(store_names)
            if invalid_stores_refs:
                raise StoreNotFoundError(
                    "Some store refs were not found in the {} store.".format(self.KIND))

    def get_stores_or_default(self, refs: List[str]):
        if refs:
            stores = self.MODEL.objects.filter(name__in=refs)
            store_names = {store.name for store in stores}
            invalid_stores_refs = set(refs) - store_names
            if invalid_stores_refs:
                raise StoreNotFoundError(
                    "Some store refs were not found in the {} store.".format(self.KIND))
            return stores
        return self.MODEL.objects.all()

    def get_paths(self, refs: List[str]):
        stores = self.get_stores_or_default(refs=refs)
        persistence_paths = {}
        for store in stores:
            persistence_paths[store.name] = store.mount_path or store.bucket
        return persistence_paths

    def get_path(self, ref: str) -> str:
        refs = [ref] if ref else None
        paths = self.get_paths(refs=refs)
        return list(paths.values())[0]

    def delete_path(self, subpath: str, ref: str):
        path = self.get_path(ref=ref)
        path = os.path.join(path, subpath)
        delete_path(path)
