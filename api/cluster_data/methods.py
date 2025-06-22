from cluster_data.schemas import ClusterDataRequest, ClusterData, ClusterDataUpload

def get_cluster_data(storage_area: dict, cluster_data_request: ClusterDataRequest) -> ClusterData:
    return ClusterData(cluster_name=cluster_data_request.cluster_name, cluster_data=storage_area[cluster_data_request.cluster_name])

def set_cluster_data(storage_area: dict, cluster_data: ClusterDataUpload) -> None:
    if cluster_data.cluster_name not in storage_area:
        storage_area[cluster_data.cluster_name] = {}
    storage_area[cluster_data.cluster_name][cluster_data.resource_type] = cluster_data.cluster_data
