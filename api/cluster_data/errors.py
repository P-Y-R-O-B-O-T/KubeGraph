from fastapi import status

CLUSTER_DATA_NOT_FOUND = {
    "status_code": status.HTTP_404_NOT_FOUND,
    "detail": "Cluster data do not exist",
}

MEMORY_UNAVAILABLE = {
    "status_code": status.HTTP_507_INSUFFICIENT_STORAGE,
    "detail": "Memory full",
}
