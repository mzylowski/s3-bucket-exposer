### Development environment

#### Local minio server as s3 backend
(Skip this step if You have already working minio, or you want to develop on your own AWS S3)
TODO


#### Clone and configure repository
* Fork and clone the repository
* Create a python3 venv and install requirements:
```
cd s3-bucket-exposer
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
* Export required configuration variables (if You need minio instance :
```
export S3_PROVIDER=minio && export S3_ACCESS_KEY="SET_ME" && export S3_SECRET_KEY="SET_ME"
```
* In the same terminal where exports are done start flask:
```
python3 -m flask run
```
* From that point from different terminal or browser you can access exposer endpoints (see documentation (TODO: link))

After every change of code flask have to be stopped by ctrl+C and restarted.
