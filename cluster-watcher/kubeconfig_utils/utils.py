import os
from kubernetes import client, config
from typing import Optional
def load_kube_config(kubeconfig_path=str)->Optional[client.Configuration]:
    
    if not os.path.exists(kubeconfig_path):
        print(f"Kubeconfig file not found at {kubeconfig_path}")
        return None
    
    try:
        configuration=client.Configuration()
        config.load_kube_config(config_file=kubeconfig_path, client_configuration=configuration)
        api_client = client.ApiClient(configuration)
        return api_client
       
    except Exception as e:
        print(f"Error loading kubeconfig: {e}")
        return None
    
    
def list_kubeconfig_files(kubeconfig_dir: str) -> list[str]:
    return [os.path.join(kubeconfig_dir, f) for f in os.listdir(kubeconfig_dir) if not f.startswith(".")]

