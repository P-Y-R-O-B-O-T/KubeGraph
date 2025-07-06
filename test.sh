#!/bin/bash

create_dot_env() {
  if [ -f ".env" ]; then
    echo ".env Exists"
    return 0
  fi
 
  echo "Creating .env ..."

  mongo_user="root"
  mongo_passwd=$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  cluster_state_api_cred_user="cluster_state_user_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  cluster_state_api_cred_passwd="cluster_state_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")

  cluster_watch_api_cred_user="cluster_watch_user_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  cluster_watch_api_cred_passwd="cluster_watch_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")

  cluster_watch_redis_cred_user="cluster_watch_user_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  cluster_watch_redis_cred_passwd="cluster_watch_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")

  cluster_state_redis_cred_user="cluster_state_user_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  cluster_state_redis_cred_passwd="cluster_state_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  
  api_redis_cred_user="api_user_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  api_redis_cred_passwd="api_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")

  graphgen_redis_cred_user="graphgen_user_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  graphgen_redis_cred_passwd="graphgen_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  
  redis_admin_user="admin_user_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  redis_admin_passwd="admin_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")
  
  admin_api_cred_user="admin"
  admin_api_cred_passwd="admin_passwd_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "32")

  api_auth_secret_key="secret_key_"$(tr -dc A-Za-z0-9 </dev/urandom | head -c "64")

  echo "MONGO_INITDB_ROOT_USERNAME=$mongo_user" >> .env
  echo "MONGO_INITDB_ROOT_PASSWORD=$mongo_passwd" >> .env
  echo "ADMIN_API_CRED_USER=$admin_api_cred_user" >> .env
  echo "ADMIN_API_CRED_PASSWD=$admin_api_cred_passwd" >> .env
  echo "CLUSTER_WATCH_API_CRED_USER=$cluster_watch_api_cred_user" >> .env
  echo "CLUSTER_WATCH_API_CRED_PASSWD=$cluster_watch_api_cred_passwd" >> .env
  echo "CLUSTER_STATE_API_CRED_USER=$cluster_state_api_cred_user" >> .env
  echo "CLUSTER_STATE_API_CRED_PASSWD=$cluster_state_api_cred_passwd" >> .env
  echo "CLUSTER_WATCH_REDIS_CRED_USER=$cluster_watch_redis_cred_user" >> .env
  echo "CLUSTER_WATCH_REDIS_CRED_PASSWD=$cluster_watch_redis_cred_passwd" >> .env
  echo "CLUSTER_STATE_REDIS_CRED_USER=$cluster_state_redis_cred_user" >> .env
  echo "CLUSTER_STATE_REDIS_CRED_PASSWD=$cluster_state_redis_cred_passwd" >> .env
  echo "API_REDIS_CRED_USER=$api_redis_cred_user" >> .env
  echo "API_REDIS_CRED_PASSWD=$api_redis_cred_passwd" >> .env
  echo "GRAPHGEN_REDIS_CRED_USER=$graphgen_redis_cred_user" >> .env
  echo "GRAPHGEN_REDIS_CRED_PASSWD=$graphgen_redis_cred_passwd" >> .env
  echo "REDIS_ADMIN_USER=$redis_admin_user" >> .env
  echo "REDIS_ADMIN_PASSWD=$redis_admin_passwd" >> .env
  echo "API_AUTH_SECRET_KEY=$api_auth_secret_key" >> .env
}

create_directory() {
  if [ -d "/kubeconf" ]; then
    echo "/kubeconf Directory exists"
    # Add commands to execute if the directory exists
  else
    sudo mkdir /kubeconf
    # Add commands to execute if the directory doesn't exist
  fi
}

build_init_db() {
    echo "Building Docker image kubegraph-init-db:latest..."
    cd init-db || exit 1
    sudo docker build --progress=plain -t kubegraph-init-db:latest .
    cd .. || exit 1
}

build_frontend() {
    echo "Building Docker image kubegraph-frontend:latest..."
    cd frontend || exit 1
    sudo docker build --progress=plain -t kubegraph-frontend:latest .
    cd .. || exit 1
}

build_cluster_state_image() {
    echo "Building Docker image kubegraph-cluster-state:latest..."
    cd cluster-state || exit 1
    sudo docker build --progress=plain -t kubegraph-cluster-state:latest .
    cd .. || exit 1
}

build_cluster_watcher_image() {
    echo "Building Docker image kubegraph-cluster-watcher:latest..."
    cd cluster-watcher || exit 1
    sudo docker build --progress=plain -t kubegraph-cluster-watcher:latest .
    cd .. || exit 1
}

build_api_image() {
    echo "Building Docker image kubegraph-api:latest..."
    cd api || exit 1
    sudo docker build --progress=plain -t kubegraph-api:latest .
    cd .. || exit 1
}

run_compose() {
    echo "Starting Docker Compose with docker-compose.test.yaml..."
    sudo docker compose -f docker-compose.test.yaml up
}

create_directory
create_dot_env
sudo docker-compose rm -f
build_frontend
build_init_db
build_cluster_state_image
build_cluster_watcher_image
build_api_image
run_compose
