#!/bin/sh

LOG_LEVEL="${LOG_LEVEL:-debug}"
DATA_DIR="${DATA_DIR:-/data}"
RDB_FILE="${RDB_FILE:-dump.rdb}"
AOF_FILE="${AOF_FILE:-appendonly.aof}"


CLUSTER_WATCH_REDIS_CRED_USER="${CLUSTER_WATCH_REDIS_CRED_USER:-default}"
CLUSTER_WATCH_REDIS_CRED_PASSWD="${CLUSTER_WATCH_REDIS_CRED_PASSWD:-default}"
API_REDIS_CRED_USER="${API_REDIS_CRED_USER:-default}"
API_REDIS_CRED_PASSWD="${API_REDIS_CRED_PASSWD:-default}"
GRAPHGEN_REDIS_CRED_USER="${GRAPHGEN_REDIS_CRED_USER:-default}"
GRAPHGEN_REDIS_CRED_PASSWD="${GRAPHGEN_REDIS_CRED_PASSWD:-default}"
REDIS_ADMIN_USER="${REDIS_ADMIN_USER:-default}"
REDIS_ADMIN_PASSWD="${REDIS_ADMIN_PASSWD:-default}"

# === Output File ===
OUTPUT_FILE="/etc/redis.conf"

# === Generate redis.conf ===
cat > "$OUTPUT_FILE" <<EOF
#####################################
# ACL USERS
#####################################
user default off
user $REDIS_ADMIN_USER on >$REDIS_ADMIN_PASSWD allkeys allcommands

user $CLUSTER_WATCH_REDIS_CRED_USER on >$CLUSTER_WATCH_REDIS_CRED_PASSWD ~RESOURCE_VERSION_BOOKMARKS:* +@read -@write
user $API_REDIS_CRED_USER on >$API_REDIS_CRED_PASSWD ~RESOURCE_VERSION_BOOKMARKS:* ~CLUSTER_DATA:* +@write ~GRAPHS:* +@read
# user $API_REDIS_CRED_USER on >$API_REDIS_CRED_PASSWD ~GRAPHS:* +@read
user $GRAPHGEN_REDIS_CRED_USER on >$GRAPHGEN_REDIS_CRED_PASSWD ~CLUSTER_DATA:* +@read ~GRAPHS:* +@write
# user $GRAPHGEN_REDIS_CRED_USER on >$GRAPHGEN_REDIS_CRED_PASSWD ~GRAPHS:* +@write

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

echo "✅ Redis configuration generated at: $OUTPUT_FILE"

redis-server /etc/redis.conf
