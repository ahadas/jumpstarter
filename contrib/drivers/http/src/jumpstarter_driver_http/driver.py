import asyncio
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import anyio
from aiohttp import web
from anyio.streams.file import FileWriteStream

from jumpstarter.driver import Driver, export

logger = logging.getLogger(__name__)


class HttpServerError(Exception):
    """Base exception for HTTP server errors"""


class FileWriteError(HttpServerError):
    """Exception raised when file writing fails"""


def get_default_ip():
    try:
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        logger.warning("Could not determine default IP address, falling back to 0.0.0.0")
        return "0.0.0.0"


@dataclass(kw_only=True)
class HttpServer(Driver):
    """HTTP Server driver for Jumpstarter"""

    root_dir: str = "/var/www"
    host: str = field(default_factory=get_default_ip)
    port: int = 8080
    app: web.Application = field(init=False, default_factory=web.Application)
    runner: Optional[web.AppRunner] = field(init=False, default=None)

    def __post_init__(self):
        super().__post_init__()
        os.makedirs(self.root_dir, exist_ok=True)
        self.app.router.add_routes([
            web.get('/{filename}', self.get_file),
        ])

    @classmethod
    def client(cls) -> str:
        """Return the import path of the corresponding client"""
        return "jumpstarter_driver_http.client.HttpServerClient"

    @export
    async def put_file(self, filename: str, src_stream) -> str:
        """
        Upload a file to the HTTP server.

        Args:
            filename (str): Name of the file to upload.
            src_stream: Stream of file content.

        Returns:
            str: Name of the uploaded file.

        Raises:
            HttpServerError: If the target path is invalid.
            FileWriteError: If the file upload fails.
        """
        try:
            file_path = os.path.join(self.root_dir, filename)

            if not Path(file_path).resolve().is_relative_to(Path(self.root_dir).resolve()):
                raise HttpServerError("Invalid target path")

            async with await FileWriteStream.from_path(file_path) as dst:
                async with self.resource(src_stream) as src:
                    async for chunk in src:
                        await dst.send(chunk)

            logger.info(f"File '{filename}' written to '{file_path}'")
            return f"{self.get_url()}/{filename}"

        except Exception as e:
            logger.error(f"Failed to upload file '{filename}': {e}")
            raise FileWriteError(f"Failed to upload file '{filename}': {e}") from e

    @export
    async def delete_file(self, filename: str) -> str:
        """
        Delete a file from the HTTP server.

        Args:
            filename (str): Name of the file to delete.

        Returns:
            str: Name of the deleted file.

        Raises:
            HttpServerError: If the file does not exist or deletion fails.
        """
        file_path = Path(self.root_dir) / filename
        if not file_path.exists():
            raise HttpServerError(f"File '{filename}' does not exist.")
        try:
            file_path.unlink()
            logger.info(f"File '{filename}' has been deleted.")
            return filename
        except Exception as e:
            logger.error(f"Failed to delete file '{filename}': {e}")
            raise HttpServerError(f"Failed to delete file '{filename}': {e}") from e

    async def get_file(self, request) -> web.FileResponse:
        """
        Retrieve a file from the HTTP server.

        Args:
            request: aiohttp request object.

        Returns:
            web.FileResponse: HTTP response containing the requested file.

        Raises:
            web.HTTPNotFound: If the requested file does not exist.
        """
        filename = request.match_info['filename']
        file_path = os.path.join(self.root_dir, filename)
        if not os.path.isfile(file_path):
            logger.warning(f"File not found: {file_path}")
            raise web.HTTPNotFound(text=f"File '{filename}' not found.")
        logger.info(f"Serving file: {file_path}")
        return web.FileResponse(file_path)

    @export
    def list_files(self) -> list[str]:
        """
        List all files in the root directory.

        Returns:
            list[str]: List of filenames in the root directory.

        Raises:
            HttpServerError: If listing files fails.
        """
        try:
            files = os.listdir(self.root_dir)
            files = [f for f in files if os.path.isfile(os.path.join(self.root_dir, f))]
            return files
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            raise HttpServerError(f"Failed to list files: {e}") from e

    @export
    async def start(self):
        """
        Start the HTTP server.

        Raises:
            HttpServerError: If the server fails to start.
        """
        if self.runner is not None:
            logger.warning("HTTP server is already running.")
            return

        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()
        logger.info(f"HTTP server started at http://{self.host}:{self.port}")

    @export
    async def stop(self):
        """
        Stop the HTTP server.

        Raises:
            HttpServerError: If the server fails to stop.
        """
        if self.runner is None:
            logger.warning("HTTP server is not running.")
            return

        await self.runner.cleanup()
        logger.info("HTTP server stopped.")
        self.runner = None

    @export
    def get_url(self) -> str:
        """
        Get the base URL of the HTTP server.

        Returns:
            str: Base URL of the HTTP server.
        """
        return f"http://{self.host}:{self.port}"

    @export
    def get_host(self) -> str:
        """
        Get the host IP address of the HTTP server.

        Returns:
            str: Host IP address.
        """
        return self.host

    @export
    def get_port(self) -> int:
        """
        Get the port number of the HTTP server.

        Returns:
            int: Port number.
        """
        return self.port

    def close(self):
        if self.runner:
            try:
                loop = asyncio.get_running_loop()
                if loop.is_running():
                    asyncio.create_task(self._async_cleanup(loop))
            except RuntimeError:
                anyio.run(self.runner.cleanup)
            self.runner = None
        super().close()

    async def _async_cleanup(self, loop):
        try:
            if self.runner:
                await self.runner.cleanup()
                logger.info("HTTP server cleanup completed asynchronously.")
        except Exception as e:
            logger.error(f"HTTP server cleanup failed asynchronously: {e}")
