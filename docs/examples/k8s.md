### Starting S3BE deployment in kubernetes

This example considers You have already working s3 backend on minio. (For AWS deployment just set `S3_PROVIDER` to AWS and remove `MINIO_ENDPOINT` env).

Apply deployment like this on your k8s cluster:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: s3be
spec:
  selector:
    matchLabels:
      run: s3be
  replicas: 2
  template:
    metadata:
      labels:
        run: s3be
    spec:
      containers:
      - name: s3be
        env:
        - name: S3_PROVIDER
          value: "minio"
        - name: MINIO_ENDPOINT
          value: "https://somes3api.domain"
        - name: S3_ACCESS_KEY
          value: "username"
        - name: S3_SECRET_KEY
          value: "password"
        - name: EXPOSER_ALLOWED_BUCKETS
          value: "downloads,sheets"
        - name: EXPOSER_TYPE
          value: "html"
        - name: EXPOSER_LOG_LEVEL
          value: "INFO"
        image: mzylowski/s3-bucket-exposer:1.0
        ports:
        - containerPort: 80
          name: s3be
```
