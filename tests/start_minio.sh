docker run -d -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=password" \
  --name minio quay.io/minio/minio server /data --console-address ":9001"
sleep 3

wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /opt/mc
chmod +x /opt/mc

export DEV_MINIO_ENDPOINT=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' minio)
/opt/mc alias set docker http://$DEV_MINIO_ENDPOINT:9000 admin password
/opt/mc mb docker/cats
/opt/mc mb docker/downloads
/opt/mc mb docker/secrets

/opt/mc cp tests/assets/cat1.jpg docker/cats
/opt/mc cp tests/assets/cat2.jpg docker/cats
/opt/mc cp tests/assets/foo.txt docker/downloads
/opt/mc cp tests/assets/secret.txt docker/secrets
