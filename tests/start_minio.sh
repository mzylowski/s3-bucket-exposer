#!/usr/bin/env bash
docker rm -f minio-local-s3

docker run -d -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=password" \
  --name minio-local-s3 quay.io/minio/minio server /data --console-address ":9001"
sleep 3

if test -f "/tmp/mc"; then
  echo "/tmp/mc already exists"
else
  wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /tmp/mc
  chmod +x /tmp/mc
fi

export DEV_MINIO_ENDPOINT=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' minio-local-s3)
/tmp/mc alias set docker http://$DEV_MINIO_ENDPOINT:9000 admin password
/tmp/mc mb docker/cats
/tmp/mc mb docker/cats/nested
/tmp/mc mb docker/downloads
/tmp/mc mb docker/secrets

/tmp/mc cp tests/assets/cat1.jpg docker/cats
/tmp/mc cp tests/assets/cat2.jpg docker/cats
/tmp/mc cp tests/assets/nested.txt docker/cats/nested
/tmp/mc cp tests/assets/foo.txt docker/downloads
/tmp/mc cp tests/assets/secret.txt docker/secrets
