
#### Configuration variables
| Variable name             | Required | Default                 | Possible values                                                                               | Description                                                                                                      |
|---------------------------|----------|-------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| `S3_PROVIDER`             | Yes      | None                    | `minio`, `aws`                                                                                | Configure your S3 backend. Only one provider can be configured. Only minio and AWS buckets are supported.        |
| `MINIO_ENDPOINT`          | No       | `http://127.0.0.1:9000` | Valid URL                                                                                     | Needs to be set when `S3_PROVIDER` is set to `minio` and your minio cluster is not configured locally.           |
| `S3_ACCESS_KEY`           | Yes      | None                    | Valid key to your s3                                                                          | Your key (sometimes considered as login) to configured S3 backend.                                               |
| `S3_SECRET_KEY`           | Yes      | None                    | Valid secret to your s3                                                                       | Your secret key (sometimes considered as password) to configured S3 backend.                                     |
| `EXPOSER_ALLOWED_BUCKETS` | No       | All accessible buckets  | List of buckets that will be exposed. Expected string with bucket names divided by semicolon. | Specify buckets You want to expose. Do not set this variable when You want expose all buckets (use with caution) |
| `EXPOSER_TYPE`            | No       | `html`                  | `empty`, `html`, `json`           | See exposers description to get more details (TODO: link)                    |
| `EXPOSER_LOG_LEVEL`            | No       | `INFO`                  | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`            | Configure log level for exposer app.  |
