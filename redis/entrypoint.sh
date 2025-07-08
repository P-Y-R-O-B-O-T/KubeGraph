#!/bin/sh

LOG_LEVEL="${LOG_LEVEL:-debug}"
DATA_DIR="${DATA_DIR:-/data}"
RDB_FILE="${RDB_FILE:-dump.rdb}"
AOF_FILE="${AOF_FILE:-appendonly.aof}"


CLUSTER_WATCH_REDIS_CRED_USER="${CLUSTER_WATCH_REDIS_CRED_USER:-default}"
CLUSTER_WATCH_REDIS_CRED_PASSWD="${CLUSTER_WATCH_REDIS_CRED_PASSWD:-default}"
CLUSTER_STATE_REDIS_CRED_USER="${CLUSTER_STATE_REDIS_CRED_USER:-default}"
CLUSTER_STATE_REDIS_CRED_PASSWD="${CLUSTER_STATE_REDIS_CRED_PASSWD:-default}"
API_REDIS_CRED_USER="${API_REDIS_CRED_USER:-default}"
API_REDIS_CRED_PASSWD="${API_REDIS_CRED_PASSWD:-default}"
GRAPHGEN_REDIS_CRED_USER="${GRAPHGEN_REDIS_CRED_USER:-default}"
GRAPHGEN_REDIS_CRED_PASSWD="${GRAPHGEN_REDIS_CRED_PASSWD:-default}"
REDIS_ADMIN_USER="${REDIS_ADMIN_USER:-default}"
REDIS_ADMIN_PASSWD="${REDIS_ADMIN_PASSWD:-default}"

# === Output File ===
OUTPUT_FILE="/etc/redis.conf"
OUTPUT_ACL_FILE="/etc/redis.acl"

# === Generate redis.conf ===
cat > "$OUTPUT_FILE" <<EOF

loadmodule /usr/local/lib/redis/modules/redisbloom.so
loadmodule /usr/local/lib/redis/modules/redisearch.so
loadmodule /usr/local/lib/redis/modules/rejson.so
loadmodule /usr/local/lib/redis/modules/redistimeseries.so

#####################################
# NETWORK
#####################################
bind 0.0.0.0
port 6379
# protected-mode yes

#####################################
# RDB SNAPSHOTS
#####################################
save 900 1
save 300 10
save 60 10000
dbfilename $RDB_FILE
dir $DATA_DIR

#####################################
# AOF
#####################################
appendonly yes
appendfilename "$AOF_FILE"
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

#####################################
# LOGGING
#####################################
loglevel $LOG_LEVEL
logfile ""
EOF

# === Generate ACL ===
cat > "$OUTPUT_ACL_FILE" <<EOF
user default off

user $REDIS_ADMIN_USER on >$REDIS_ADMIN_PASSWD allkeys allcommands +auth +ping +select +echo +info

user $CLUSTER_WATCH_REDIS_CRED_USER on >$CLUSTER_WATCH_REDIS_CRED_PASSWD +@read +@write %RW~CLUSTER_DATA:*  %RW~RESOURCE_VERSION_BOOKMARKS:*
user $CLUSTER_STATE_REDIS_CRED_USER on >$CLUSTER_STATE_REDIS_CRED_PASSWD +@read +@write %RW~CLUSTER_DATA:*  %RW~RESOURCE_VERSION_BOOKMARKS:*

user $API_REDIS_CRED_USER on >$API_REDIS_CRED_PASSWD +@read +@write %RW~RESOURCE_VERSION_BOOKMARKS:* %RW~CLUSTER_DATA:* %R~GRAPHS:*

user $GRAPHGEN_REDIS_CRED_USER on >$GRAPHGEN_REDIS_CRED_PASSWD +@read +@write %R~CLUSTER_DATA:* %W~GRAPHS:*

EOF

redis-server /etc/redis.conf --aclfile /etc/redis.acl
