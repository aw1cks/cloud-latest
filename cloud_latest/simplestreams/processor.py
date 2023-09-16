from functools import cached_property
from typing import Generator, List

from cloud_latest.image import Platform, get_image_type
from cloud_latest.image.architecture import CPUArchitecture
from cloud_latest.simplestreams import Stream
from cloud_latest.simplestreams.download import Download
from cloud_latest.simplestreams.product import Product
from cloud_latest.simplestreams.release import Release


class StreamProcessor:
    def __init__(self, stream: Stream, **kwargs) -> None:
        self._stream = stream

        platform: str = kwargs.get("platform", "generic")
        self._platform = Platform[platform]  # type: ignore

        image_type: str = kwargs.get("image_type", "")
        self._image_type: str = get_image_type(self._platform, image_type)

        arch: str = kwargs.get("arch", "amd64")
        self._arch = CPUArchitecture(arch)

        self._version: str = kwargs.get("version", "latest")

    @cached_property
    def _products(self) -> List[Product]:
        return list(self._stream.products.values())

    def _products_matching_arch(self, products: List[Product]) -> Generator[Product, None, None]:
        for product in products:
            if product.arch == self._arch.value:
                yield product

    def _products_matching_version(self, products: List[Product]) -> Generator[Product, None, None]:
        for product in products:
            if product.match_version(self._version):
                yield product

    def _validate_product_list(self, products: List[Product]) -> List[Product]:
        if len(products) < 1:
            errmsg = f"No OS release found for version '{self._version}', architecture '{self._arch.name}'"
            raise ValueError(errmsg)

        return products

    @cached_property
    def product(self) -> Product:
        products = list(self._products_matching_arch(self._products))

        if self._version == "latest":
            return self._validate_product_list(products)[-1]

        products_matching_version = list(self._products_matching_version(products))
        return self._validate_product_list(products_matching_version)[-1]

    @cached_property
    def latest_release(self) -> Release:
        return list(self.product.versions.values())[-1]

    @cached_property
    def download(self) -> Download:
        try:
            return self.latest_release.items[self._image_type]
        except KeyError as e:
            errmsg = (
                f"OS '{self._version}', architecture '{self._arch.name}' "
                f"does not support platform '{self._platform.name}'"
            )
            raise ValueError(errmsg) from e
