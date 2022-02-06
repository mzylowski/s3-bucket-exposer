### Development environment

#### Clone and virtual env installation
* (Fork and) clone the repository
* Create a python3 venv and install requirements:
```
cd s3-bucket-exposer
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r s3-bucket-exposer/requirements.txt
```
From this place You can also install tests requirements (if needed):
```
pip3 install -r tests-requirements.txt
```

To run S3BE we need s3 backend. Skip next step if You want to use Your own S3 for developing.

#### Local minio server as s3 backend
**Automatic way:**
You can use the same script that S3BE CI is using:
```
./tests/start_minio.sh
```
**Manual way:**
If You don't want to run minio by bash script You can do it manually:
```
docker run -d -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=password" \
  --name minio-local-s3 quay.io/minio/minio server /data --console-address ":9001"
```
When minio is running, let's get IP of the container:
```
export DEV_MINIO_ENDPOINT=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' minio-local-s3)
```

#### Start flask application
* Go to python app repository:
```
cd s3-bucket-exposer
```
* Export required configuration variables (if configuring local minio use):
```
export S3_PROVIDER=minio && export S3_ACCESS_KEY="admin" && export S3_SECRET_KEY="password" && export MINIO_ENDPOINT="http://$DEV_MINIO_ENDPOINT:9000"
```
* In the same terminal where exports are made start flask:
```
python3 -m flask run
```
* From that point, from different terminal or browser you can access exposer endpoints ([see documentation](../README.md#endpoints) for valid endpoints).

(After every change of code, flask have to be stopped by ctrl+C and restarted.)
