import base64
import os
import ssl
from urllib.parse import urlparse

import grpc


def ssl_channel_credentials(target: str, insecure: bool = False, ca_certificate: str = ""):
    if insecure or os.getenv("JUMPSTARTER_GRPC_INSECURE") == "1":
        parsed = urlparse(f"//{target}")
        port = parsed.port if parsed.port else 443
        root_certificates = ssl.get_server_certificate((parsed.hostname, port))
        return grpc.ssl_channel_credentials(root_certificates=root_certificates.encode())
    elif ca_certificate != "":
        # convert ca_certificate base64 encoded to pem encoded string
        ca_certificate = base64.b64decode(ca_certificate)
        return grpc.ssl_channel_credentials(ca_certificate)
    else:
        return grpc.ssl_channel_credentials()


def aio_secure_channel(target: str, credentials: grpc.ChannelCredentials):
    return grpc.aio.secure_channel(target, credentials, options=(("grpc.lb_policy_name", "round_robin"),))
