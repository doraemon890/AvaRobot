import asyncio
import os
from typing import Optional

import aiofiles
import aiohttp


class DownloadJob:

    def __init__(
        self,
        session: aiohttp.ClientSession,
        file_url: str,
        save_path: Optional[str] = None,
        chunk_size: Optional[int] = 1024,
    ):
        self.file_url = file_url
        self._session = session
        self._chunk_size = chunk_size

        self.file_name = file_url.split("/")[~0][:230]
        self.file_path = (
            os.path.join(save_path, self.file_name) if save_path else self.file_name
        )

        self.completed = False
        self.progress = 0
        self.size = 0

    async def get_size(self) -> int:
        if not self.size:
            async with self._session.get(self.file_url) as resp:
                if 200 <= resp.status < 300:
                    self.size = int(resp.headers["Content-Length"])

                else:
                    raise aiohttp.errors.HttpProcessingError(
                        message=f"There was a problem processing {self.file_url}",
                        code=resp.status,
                    )

        return self.size

    def _downloaded(self, chunk_size):
        self.progress += chunk_size

    async def download(self):
        async with self._session.get(self.file_url) as resp:
            # Checkning the response code
            if 200 <= resp.status < 300:
                # Saving the data to the file chunk by chunk.
                async with aiofiles.open(self.file_path, "wb") as file:
                    # Downloading the file using the aiohttp.StreamReader
                    async for data in resp.content.iter_chunked(self._chunk_size):
                        await file.write(data)
                        self._downloaded(self._chunk_size)

                self.completed = True
                return self
            raise aiohttp.errors.HttpProcessingError(
                message=f"There was a problem processing {self.file_url}",
                code=resp.status,
            )


class Handler:
    def __init__(
        self,
        loop: Optional[asyncio.BaseEventLoop] = None,
        session: Optional[aiohttp.ClientSession] = None,
        chunk_size: Optional[int] = 1024,
    ):
        self._loop = loop or asyncio.get_event_loop()
        self._session = session or aiohttp.ClientSession(loop=self._loop)
        self._chunk_size = chunk_size

    def _job_factory(
        self, file_url: str, save_path: Optional[str] = None
    ) -> DownloadJob:
        return DownloadJob(self._session, file_url, save_path, self._chunk_size)

    async def download(self, url: str, save_path: Optional[str] = None) -> DownloadJob:

        job = self._job_factory(url, save_path=save_path)

        task = asyncio.ensure_future(job.download())

        await task
        file_name = url.split("/")[-1]
        file_name = file_name[:230] if len(file_name) > 230 else file_name
        return save_path or f"{os.getcwd()}/{file_name}"
