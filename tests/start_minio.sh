#!/usr/bin/env bash
docker rm -f minio-local-s3

docker run -d -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=password" \
  --name minio-local-s3 quay.io/minio/minio server /data --console-address ":9001"
sleep 3

if test -f "/opt/mc"; then
  echo "/opt/mc already exists"
else
  wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /opt/mc
  chmod +x /opt/mc
fi

export DEV_MINIO_ENDPOINT=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' minio-local-s3)
/opt/mc alias set docker http://$DEV_MINIO_ENDPOINT:9000 admin password
/opt/mc mb docker/cats
/opt/mc mb docker/cats/nested
/opt/mc mb docker/downloads
/opt/mc mb docker/secrets

/opt/mc cp tests/assets/cat1.jpg docker/cats
/opt/mc cp tests/assets/cat2.jpg docker/cats
/opt/mc cp tests/assets/nested.txt docker/cats/nested
/opt/mc cp tests/assets/foo.txt docker/downloads
/opt/mc cp tests/assets/secret.txt docker/secrets
