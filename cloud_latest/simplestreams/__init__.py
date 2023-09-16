import datetime
import typing
from typing import Final

import pydantic

from cloud_latest.simplestreams.product import Product

# fmt: off
UBUNTU_CLOUD_CONTENT_ID: Final[str]  = "com.ubuntu.cloud:released:download"
UBUNTU_CLOUD_DATATYPE: Final[str]    = "image-downloads"
UBUNTU_CLOUD_FORMAT: Final[str]      = "products:1.0"
UBUNTU_CLOUD_DATE_FORMAT: Final[str] = "%a, %d %b %Y %H:%M:%S %z"
#                      %a -> abbreviated day of week
#                          %d -> numerical day of month
#                             %b -> abbreviated month
#                                %Y -> full year incl. century
#                                   %H -> hour of day (24hr)
#                                      %M -> minute
#                                         %S -> second
#                                            %z -> time zone offset
# See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
# fmt: on

"""
Data model for Ubuntu cloud image simplestreams.

Pydantic models to represent the cloud image feed.
It uses simplestreams: https://launchpad.net/simplestreams

The data is represented as JSON which we deserialize from these models.

See https://cloud-images.ubuntu.com/releases/streams/v1/com.ubuntu.cloud:released:download.json
"""


class Stream(pydantic.BaseModel):
    """
    content_id='com.ubuntu.cloud:released:download',
    datatype='image-downloads',
    format='products:1.0',
    """

    content_id: str = pydantic.Field(..., repr=False)
    datatype: str = pydantic.Field(..., repr=False)
    format: str = pydantic.Field(..., repr=False)  # noqa: A003
    # Dates are returned thusly:
    # 'Thu, 14 Sep 2023 07:45:07 +0000'
    updated: datetime.datetime
    products: typing.Mapping[str, Product]

    @pydantic.field_validator("content_id", mode="after")
    @classmethod
    def ensure_content_id_ubuntu_cloud(cls, val):
        if val != UBUNTU_CLOUD_CONTENT_ID:
            errmsg = f"content_id '{val}' does not match expected '{UBUNTU_CLOUD_CONTENT_ID}'"
            raise ValueError(errmsg)

        return val

    @pydantic.field_validator("datatype", mode="after")
    @classmethod
    def ensure_datatype_image_downloads(cls, val):
        if val != UBUNTU_CLOUD_DATATYPE:
            errmsg = f"datatype '{val}' does not match expected '{UBUNTU_CLOUD_DATATYPE}'"
            raise ValueError(errmsg)

        return val

    @pydantic.field_validator("format", mode="after")
    @classmethod
    def ensure_format(cls, val):
        if val != UBUNTU_CLOUD_FORMAT:
            errmsg = f"format '{val}' does not match expected '{UBUNTU_CLOUD_FORMAT}'"
            raise ValueError(errmsg)

        return val

    # This field_validator runs to convert the non-standard date format
    # See the `DEFAULT_DATE_FORMAT` const
    @pydantic.field_validator("updated", mode="before")
    @classmethod
    def ensure_updated_field_is_datetime(cls, val):
        if isinstance(val, str):
            # https://github.com/astral-sh/ruff/issues/7488
            return datetime.datetime.strptime(val, UBUNTU_CLOUD_DATE_FORMAT)  # noqa: DTZ007

        return val


class JsonStream(pydantic.BaseModel):
    stream: pydantic.Json[Stream]
