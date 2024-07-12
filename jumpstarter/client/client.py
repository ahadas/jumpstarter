from jumpstarter.v1 import jumpstarter_pb2, jumpstarter_pb2_grpc, router_pb2_grpc
from jumpstarter.drivers import DriverStub
from google.protobuf import empty_pb2
from dataclasses import dataclass
import jumpstarter.drivers as drivers


@dataclass
class Client:
    stub: jumpstarter_pb2_grpc.ExporterServiceStub

    def __init__(self, channel):
        self.stub = jumpstarter_pb2_grpc.ExporterServiceStub(channel)
        self.router = router_pb2_grpc.RouterServiceStub(channel)

    async def sync(self):
        devices = dict()
        for device in (await self.GetReport()).device_report:
            stub = self.GetDevice(device)
            devices[stub.uuid] = stub
            if device.parent_device_uuid == "":
                setattr(self, stub.labels["jumpstarter.dev/name"], stub)
            else:
                setattr(
                    devices[device.parent_device_uuid],
                    stub.labels["jumpstarter.dev/name"],
                    stub,
                )

    async def GetReport(self):
        return await self.stub.GetReport(empty_pb2.Empty())

    def GetDevice(self, report: jumpstarter_pb2.DeviceReport):
        base = drivers.get(report.driver_interface)

        class stub_class(DriverStub, base=base):
            pass

        return stub_class(stub=self.stub, uuid=report.device_uuid, labels=report.labels)
