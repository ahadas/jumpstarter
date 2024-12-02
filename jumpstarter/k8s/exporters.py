from typing import Optional

from kubernetes import client


class ExportersV1Alpha1Api:
    """Interact with the exporters custom resource API"""
    api: client.CustomObjectsApi

    def __init__(self):
        self.api = client.CustomObjectsApi()

    def get_namespaced_exporters(self, namespace: str):
        """List the exporter objects in the cluster."""
        res = self.api.list_namespaced_custom_object(
            namespace=namespace,
            group="jumpstarter.dev",
            plural="exporters",
            version="v1alpha1"
        )
        return res["items"]

    def get_namespaced_exporter(self, namespace: str, name: str) -> Optional[object]:
        """Get a single exporter object from the cluster."""
        res = self.api.get_namespaced_custom_object(
            namespace=namespace,
            group="jumpstarter.dev",
            plural="exporters",
            version="v1alpha1",
            name=name
        )
        return res
