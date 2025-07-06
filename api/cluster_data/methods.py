from cluster_data.schemas import (
    ClusterDataRequest,
    ClusterData,
    ClusterDataUpload,
    ObjectDataUpload,
)
from cluster_data.errors import (
    CLUSTER_DATA_NOT_FOUND,
    MEMORY_UNAVAILABLE,
    CLUSTER_NOT_EXIST_YET,
    RESOURCE_TYPE_NOT_EXIST_IN_CLUSTER,
)
from fastapi import HTTPException
import traceback


def get_cluster_data(
    storage_area: dict, cluster_data_request: ClusterDataRequest
) -> ClusterData:
    if cluster_data_request.cluster_name not in storage_area:
        raise HTTPException(**CLUSTER_DATA_NOT_FOUND)
    return ClusterData(
        cluster_name=cluster_data_request.cluster_name,
        cluster_data=storage_area[cluster_data_request.cluster_name],
    )


def set_cluster_data(storage_area: dict, cluster_data: ClusterDataUpload) -> None:
    try:
        if cluster_data.cluster_name not in storage_area:
            storage_area[cluster_data.cluster_name] = {}
        if cluster_data.resource_type not in storage_area[cluster_data.cluster_name]:
            storage_area[cluster_data.cluster_name][cluster_data.resource_type] = {}

        for _ in cluster_data.cluster_data:
            if (
                _
                not in storage_area[cluster_data.cluster_name][
                    cluster_data.resource_type
                ]
            ):
                storage_area[cluster_data.cluster_name][cluster_data.resource_type][
                    _
                ] = cluster_data.cluster_data[_]
                continue
            if int(cluster_data.cluster_data[_]["metadata"]["resource_version"]) >= int(
                storage_area[cluster_data.cluster_name][cluster_data.resource_type][_][
                    "metadata"
                ]["resource_version"]
            ):
                storage_area[cluster_data.cluster_name][cluster_data.resource_type][
                    _
                ] = cluster_data.cluster_data[_]
    except:
        raise HTTPException(**MEMORY_UNAVAILABLE)


def update_cluster_objects(storage_area: dict, object_data: ObjectDataUpload) -> None:
    if object_data.cluster_name not in storage_area:
        raise HTTPException(**CLUSTER_NOT_EXIST_YET)
    if object_data.resource_type not in storage_area[object_data.cluster_name]:
        raise HTTPException(**RESOURCE_TYPE_NOT_EXIST_IN_CLUSTER)
    try:
        if object_data.event_type == "ADDED":
            if (
                object_data.resource_uid
                in storage_area[object_data.cluster_name][object_data.resource_type]
            ):
                if (
                    object_data.object_data["metadata"]["resource_version"]
                    > storage_area[object_data.cluster_name][object_data.resource_type][
                        object_data.resource_uid
                    ]["metadata"]["resource_version"]
                ):
                    storage_area[object_data.cluster_name][object_data.resource_type][
                        object_data.resource_uid
                    ] = object_data.object_data
            else:
                storage_area[object_data.cluster_name][object_data.resource_type][
                    object_data.resource_uid
                ] = object_data.object_data

        if object_data.event_type == "DELETED":
            if (
                object_data.resource_uid
                in storage_area[object_data.cluster_name][object_data.resource_type]
            ):
                del storage_area[object_data.cluster_name][object_data.resource_type][
                    object_data.resource_uid
                ]

        if object_data.event_type == "MODIFIED":
            if (
                object_data.resource_uid
                not in storage_area[object_data.cluster_name][object_data.resource_type]
            ):
                return
            if (
                object_data.object_data["metadata"]["resource_version"]
                > storage_area[object_data.cluster_name][object_data.resource_type][
                    object_data.resource_uid
                ]["metadata"]["resource_version"]
            ):
                storage_area[object_data.cluster_name][object_data.resource_type][
                    object_data.resource_uid
                ] = object_data.object_data

    except:
        raise HTTPException(**MEMORY_UNAVAILABLE)
