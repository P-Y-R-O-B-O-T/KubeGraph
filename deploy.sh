#!/bin/bash

cd cluster-state

sudo docker build --progress=plain -t kubegraph-cluster-state:latest .
