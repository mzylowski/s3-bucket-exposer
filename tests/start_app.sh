#!/usr/bin/env bash
docker rm -f s3-bucket-exposer

export DEV_MINIO_ENDPOINT=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' minio-local-s3)
docker run -d -p 80:80 \
  --name s3-bucket-exposer \
  -e S3_PROVIDER="minio" \
  -e S3_ACCESS_KEY="admin" \
  -e S3_SECRET_KEY="password" \
  -e MINIO_ENDPOINT="http://$DEV_MINIO_ENDPOINT:9000" \
  -e EXPOSER_ALLOWED_BUCKETS="cats, downloads" \
  -e EXPOSER_TYPE=$1 s3-bucket-exposer
