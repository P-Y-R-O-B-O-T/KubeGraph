from cluster_data.schemas import ClusterDataRequest, ClusterData

def get_cluster_data(storage_area: dict, cluster_data_request: ClusterDataRequest) -> ClusterData:
    return ClusterData(cluster_name=cluster_data_request.cluster_name, cluster_data=storage_area[cluster_data_request.cluster_name])
