### Development environment

#### Local minio server as s3 backend
If you don't want to develop on your already configured s3 backend, we can configure local minio:
```
docker run -d -p 9000:9000 -p 9001:9001 \
    -e "MINIO_ROOT_USER=admin" \
    -e "MINIO_ROOT_PASSWORD=password" \
    --name minio quay.io/minio/minio server /data --console-address ":9001"
```

#### Clone and configure repository
* Fork and clone the repository
* Create a python3 venv and install requirements:
```
cd s3-bucket-exposer
python3 -m venv .venv
source .venv/bin/activate
cd s3-bucket-exposer #we going to python app directory
pip3 install -r requirements.txt
```
* Export required configuration variables (if configuring local minio use):
```
export S3_PROVIDER=minio && export S3_ACCESS_KEY="admin" && export S3_SECRET_KEY="password"
```
* In the same terminal where exports are done start flask:
```
python3 -m flask run
```
* From that point, from different terminal or browser you can access exposer endpoints (see documentation (TODO: link))

(After every change of code, flask have to be stopped by ctrl+C and restarted.)
