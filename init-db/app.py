import pymongo
import os
import time
import traceback
from passlib.context import CryptContext

time.sleep(5)

print(os.getenv("MONGO_INITDB_ROOT_USERNAME"))
print(os.getenv("MONGO_INITDB_ROOT_PASSWORD"))
print(os.getenv("ADMIN_API_CRED_USER"))
print(os.getenv("ADMIN_API_CRED_PASSWD"))
print(os.getenv("CLUSTER_WATCH_API_CRED_USER"))
print(os.getenv("CLUSTER_WATCH_API_CRED_PASSWD"))
print(os.getenv("CLUSTER_STATE_API_CRED_USER"))
print(os.getenv("CLUSTER_STATE_API_CRED_PASSWD"))

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

CLIENT = pymongo.MongoClient(
    f"mongodb://{os.getenv("MONGO_INITDB_ROOT_USERNAME")}:{os.getenv("MONGO_INITDB_ROOT_PASSWORD")}@mongo:27017"
)

USERS_DB = CLIENT["USERS"]
USERS_COLLECTION = USERS_DB["USERS"]

admin_user = USERS_COLLECTION.find_one({"username": os.getenv("ADMIN_API_CRED_USER")})
cluster_state_user = USERS_COLLECTION.find_one(
    {"username": os.getenv("CLUSTER_STATE_API_CRED_USER")}
)
cluster_watch_user = USERS_COLLECTION.find_one(
    {"username": os.getenv("CLUSTER_WATCH_API_CRED_USER")}
)

print(admin_user, cluster_state_user, cluster_watch_user)

if admin_user is None:
    try:
        USERS_COLLECTION.insert_one(
            {
                "username": os.getenv("ADMIN_API_CRED_USER"),
                "hashed_password": PWD_CONTEXT.hash(
                    str(os.getenv("ADMIN_API_CRED_PASSWD"))
                ),
                "internal": False,
                "disbled": False,
            }
        )
        print("Created admin user")
    except:
        traceback.print_exc()
if cluster_state_user is None:
    try:
        USERS_COLLECTION.insert_one(
            {
                "username": os.getenv("CLUSTER_WATCH_API_CRED_USER"),
                "hashed_password": PWD_CONTEXT.hash(
                    str(os.getenv("CLUSTER_WATCH_API_CRED_PASSWD"))
                ),
                "internal": True,
                "disbled": False,
            }
        )
        print("Created cluster watch user")
    except:
        traceback.print_exc()
if cluster_watch_user is None:
    try:
        USERS_COLLECTION.insert_one(
            {
                "username": os.getenv("CLUSTER_STATE_API_CRED_USER"),
                "hashed_password": PWD_CONTEXT.hash(
                    str(os.getenv("CLUSTER_STATE_API_CRED_PASSWD"))
                ),
                "internal": True,
                "disbled": False,
            }
        )
        print("Created cluster state user")
    except:
        traceback.print_exc()
