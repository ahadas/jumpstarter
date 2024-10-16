import sys
from base64 import b64encode
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from shutil import which
from subprocess import Popen, TimeoutExpired
from tempfile import TemporaryDirectory

from aiohttp import ClientSession, UnixConnector
from anyio import connect_unix

from jumpstarter.driver import Driver, export, exportstream

from .common import UStreamerState


def find_ustreamer():
    executable = which("ustreamer")

    if executable is None:
        raise FileNotFoundError("ustreamer executable not found")

    return executable


@dataclass(kw_only=True)
class UStreamer(Driver):
    executable: str = field(default_factory=find_ustreamer)
    args: dict[str, str] = field(default_factory=dict)
    tempdir: TemporaryDirectory = field(default_factory=TemporaryDirectory)

    @classmethod
    def client(cls) -> str:
        return "jumpstarter_driver_ustreamer.client.UStreamerClient"

    def __post_init__(self):
        super().__post_init__()

        cmdline = [self.executable]

        for key, value in self.args.items():
            cmdline += [f"--{key}", value]

        self.socketp = Path(self.tempdir.name) / "socket"

        cmdline += ["--unix", self.socketp]

        self.process = Popen(cmdline, stdout=sys.stdout, stderr=sys.stderr)

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except TimeoutExpired:
            self.process.kill()

    @export
    async def state(self):
        async with ClientSession(connector=UnixConnector(path=self.socketp)) as session:
            async with session.get("http://localhost/state") as r:
                return UStreamerState.model_validate(await r.json())

    @export
    async def snapshot(self):
        async with ClientSession(connector=UnixConnector(path=self.socketp)) as session:
            async with session.get("http://localhost/snapshot") as r:
                return b64encode(await r.read()).decode("ascii")

    @exportstream
    @asynccontextmanager
    async def connect(self):
        async with await connect_unix(self.socketp) as stream:
            yield stream