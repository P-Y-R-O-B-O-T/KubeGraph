
from typing import Optional

def get_list_method(self, core_v1_api, resource_name: str) -> Optional[callable]:
       
        mapping = {
            "pods": core_v1_api.list_pod_for_all_namespaces,
            "nodes": core_v1_api.list_node,
            "services": core_v1_api.list_service_for_all_namespaces,
            "namespaces": core_v1_api.list_namespace,
          
        }
        return mapping.get(resource_name)