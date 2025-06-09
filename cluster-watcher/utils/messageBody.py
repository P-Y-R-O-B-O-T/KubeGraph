from typing import Optional,Dict
class MessageBody:
    def __init__(self, resource: str, cluster_name: str, namespace: Optional[str] = None, event: Optional[Dict] = None):
        self.resource = resource
        self.cluster_name = cluster_name
        self.namespace = namespace
        self.type = event.get("type") if event else None
        obj = event.get("object") if event else None
        if hasattr(obj, "to_dict"):
            self.object = obj.to_dict()
        else:
            self.object = str(obj) if obj else None

    def get_body(self):
        data = {
            "resource": self.resource,
            "cluster_name": self.cluster_name,
            "namespace": self.namespace,
            "type": self.type,
            "object": self.object,
        }
        return data


def create_message(resource: str, cluster_name: str, namespace: Optional[str] = None, event: Optional[Dict] = None) -> MessageBody:
    return MessageBody(resource, cluster_name, namespace, event)
