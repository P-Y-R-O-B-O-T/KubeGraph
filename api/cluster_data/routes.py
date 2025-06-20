#
from fastapi import Depends
from cluster_data.schemas import ClusterDataType
from authentication.auth import AuthService
from authentication.schemas import User
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter


# class ClusterDataRoutes:
#     def __init__(self) -> None:
#         self.AUTH_MECHANISM = AuthService()
#         self.ROUTER = APIRouter(prefix="/cluster", tags=["cluster_data"])

#         self.ROUTER.get("/{clustername}/{resourcetype}", response_model=ClusterDataType)(ClusterDataRoutes.upload_cluster_data)
    
    
#     async def upload_cluster_data(
#         self,
#         clustername: str,
#         resourcetype: str,
#         current_user: Annotated[User, Depends(AuthService().get_current_active_user)],
#         # or current_user=Depends(AuthService().get_current_active_user)
#     ):
        
#         return ClusterDataType(
#             username=current_user,
#             content={
#                 "key-1": "Value of key-1"
#             }
#         )

# class ClusterDataRoutes:
#     AUTH_MECHANISM = AuthService()
#     ROUTER = APIRouter(prefix="/cluster", tags=["cluster_data"])

#     @ROUTER.get("/{clustername}/{resourcetype}", response_model=ClusterDataType)
#     @staticmethod
#     async def upload_cluster_data(
#         clustername: str,
#         resourcetype: str,
#         current_user: Annotated[User, Depends(lambda: ClusterDataRoutes.AUTH_MECHANISM.get_current_active_user())],
#     ):
#         return ClusterDataType(
#             username=current_user.username,
#             content={"key-1": f"Data for {clustername} and {resourcetype}"}
#         )



# class ClusterDataRoutes:
#     AUTH_MECHANISM = AuthService()
#     ROUTER = APIRouter(prefix="/cluster", tags=["cluster_data"])

#     # No changes are needed in the route decorator itself, because the dependency
#     # chain now correctly informs FastAPI/OpenAPI about the security requirements.
#     @ROUTER.get("/{clustername}/{resourcetype}", response_model=ClusterDataType)
#     @staticmethod
#     async def get_cluster_data(
#         clustername: str,
#         resourcetype: str,
#         # This dependency now correctly triggers the OpenAPI security scheme
#         current_user: Annotated[User, Depends(AUTH_MECHANISM.get_current_active_user)],
#     ):
#         return ClusterDataType(
#             username=current_user.username,
#             content={"key-1": f"Data for {clustername} and {resourcetype}"}
#         )


# class ClusterDataRoutes:
#     def __init__(self) -> None:
#         self.ROUTER = APIRouter(prefix="/cluster", tags=["cluster_data"])

#         self.ROUTER.get("/{clustername}/{resourcetype}", response_model=ClusterDataType)(
#             self.upload_cluster_data
#         )

#     async def upload_cluster_data(
#         self,
#         clustername: str,
#         resourcetype: str,
#         # current_user: Annotated[User, Depends(AuthService().get_current_active_user)],
#     ):
#         """
#         Handles the API request to get cluster data.
#         """
#         print(f"Instance method called for cluster: {clustername}")
        
#         return ClusterDataType(
#             username=current_user.username,
#             content={
#                 "cluster": clustername,
#                 "resource": resourcetype,
#                 "key-1": "Value of key-1"
#             }
#         )


class ClusterDataRoutes:
    def __init__(self):
        self. ROUTER = APIRouter (prefix="/cluster", tags=["cluster_data"])
        self.ROUTER.add_api_route(
            "/{clustername}/{resourcetype}",
            self.upload_cluster_data,
            methods=["GET"],
            response_model=ClusterDataType
        )
        async def upload_cluster_data(self, clustername: str, resourcetype: str): 
            print (f"Instance method called for cluster: {clustername}")
            return ClusterDataType(
                username="dummy_user",
                content={
                    "cluster": clustername,
                    "resource": resourcetype, 
                    "key-1": "Value of key-1"
                }
            )
    