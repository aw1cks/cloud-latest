from functools import cached_property
from typing import Final

import httpx

from cloud_latest.net import DEFAULT_TIMEOUT
from cloud_latest.simplestreams import JsonStream, Stream
from cloud_latest.simplestreams.download import Download

# fmt: off
DEFAULT_URL: Final[str]         = "https://cloud-images.ubuntu.com"
DEFAULT_STREAM_PATH: Final[str] = "releases/streams/v1/com.ubuntu.cloud:released:download.json"
# fmt: on


class Mirror:
    def __init__(self, **kwargs) -> None:
        self.url = kwargs.get("url", DEFAULT_URL)
        self._stream_path = kwargs.get("stream_path", DEFAULT_STREAM_PATH)

        httpx_config = kwargs.get("httpx_config", {"timeout": DEFAULT_TIMEOUT})
        self._http_client = httpx.Client(**httpx_config)

    def __del__(self):
        self._http_client.close()

    @cached_property
    def _stream_url(self) -> str:
        return f"{self.url}/{self._stream_path}"

    @cached_property
    def _stream_raw_json(self) -> str:
        return self._http_client.get(self._stream_url).text

    @cached_property
    def stream(self) -> Stream:
        j = JsonStream(stream=self._stream_raw_json)  # type: ignore
        return j.stream

    def get_download_url(self, dl: Download) -> str:
        return f"{self.url}/{dl.path}"
