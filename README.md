[![S3BE tests](https://github.com/mzylowski/s3-bucket-exposer/actions/workflows/functional.yml/badge.svg)](https://github.com/mzylowski/s3-bucket-exposer/actions/workflows/functional.yml)

## S3 Bucket Exposer (S3BE)

S3BE is a small containerized python app that allows You to expose objects from S3 buckets to local network or internet. This tool can change your S3 buckets to file sharing platform without switching buckets to public.
App allows downloading objects from S3 storage by generating presigned URL's and redirecting to them. After redirection, file is downloaded and link becomes inactive.

#### Supported S3 operators (providers)
* minio
* AWS

#### S3BE Exposers
S3BE allows You to choose one exposer from given list:
* Empty (`empty`) - this exposer won't print any data in HTML body. List of buckets and objects won't be shown in response, so downloading files will be possible only when proper endpoint is specified. This is recommended if you're exposing bucket to the internet.
* HTML (`html`) - list of buckets and files will be exposed and visible in browser (in HTML response). This exposer also allows to browse objects in buckets.
* JSON (`json`) - NotImplementedYet but planned: #10

#### Endpoints
* `/` - returns list of buckets
* `/bucket/<bucket_name>` - returns list of objects in <bucket_name>
* `/download/<bucket_name>/<path>` - redirects to download URL for object (path) from bucket (bucket_name). 

#### Configuration variables
| Variable name             | Required | Default                 | Possible values                                                                           | Description                                                                                                                        |
|---------------------------|----------|-------------------------|-------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `S3_PROVIDER`             | Yes      | None                    | `minio`, `aws`                                                                            | Configure your S3 backend. Only one provider can be configured. Only minio and AWS backends are supported.                         |
| `MINIO_ENDPOINT`          | No       | `http://127.0.0.1:9000` | Valid URL                                                                                 | Needs to be set when `S3_PROVIDER` is set to `minio` and your minio cluster is not configured locally.                             |
| `S3_ACCESS_KEY`           | Yes      | None                    | Valid key to your s3                                                                      | Your key (sometimes considered as login) to configured S3 backend.                                                                 |
| `S3_SECRET_KEY`           | Yes      | None                    | Valid secret to your s3                                                                   | Your secret key (sometimes considered as password) to configured S3 backend.                                                       |
| `EXPOSER_ALLOWED_BUCKETS` | No       | All accessible buckets  | List of buckets that will be exposed. Expected string with bucket names divided by comma. | Specify list of buckets You want to expose. Do not set this variable when You want expose all buckets (use with caution).          |
| `EXPOSER_TYPE`            | No       | `html`                  | `empty`, `html`, `json`                                                                   | See exposers description to get more [details](README.md#s3be-exposers).                                                           |
| `EXPOSER_LOG_LEVEL`       | No       | `ERROR`                 | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`, `OFF`                                    | Configure log level for exposer app. To turn off logging from s3-bucket-exposer set var to OFF. uWSGI logging won't be turned off. |

#### Examples
Check our examples related with running S3BE:
* Docker
* Kubernetes
* AWS S3 example (docker)

#### Contribution
Issues or Contributions and Pull-Requests are welcome!
Check [devel](docs/devel.md) instruction for running development environment.
