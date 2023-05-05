from typing import Optional

from torch import Tensor

from ..utils import interp2d
from .base import Source

__all__ = ("ImageSource",)


class ImageSource(Source):
    def __init__(
        self,
        name: str,
        thx0: Optional[Tensor] = None,
        thy0: Optional[Tensor] = None,
        image: Optional[Tensor] = None,
        scale: Optional[Tensor] = None,
        image_shape: Optional[tuple[int, ...]] = None,
    ):
        super().__init__(name)
        self.add_param("thx0", thx0)
        self.add_param("thy0", thy0)
        self.add_param("image", image, image_shape)
        self.add_param("scale", scale)

    def brightness(self, thx, thy, x):
        thx0, thy0, image, scale = self.unpack(x)
        return interp2d(
            image, (thx - thx0).view(-1) / scale, (thy - thy0).view(-1) / scale
        ).reshape(thx.shape)