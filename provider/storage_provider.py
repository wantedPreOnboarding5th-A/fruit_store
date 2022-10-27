from django.conf import settings

# S3 이미지 업로드 관련 클래스 구현

class AmazonS3Provider:
    def __init__(self) -> None:
        self.default_file_storage = 'storages.backends.s3boto3.S3Boto3Storage'
        self.aws_access_key_id = 'AKIA2Z7E4H24OEU34B7H'
        self.aws_secret_access_key = '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'
        self.aws_storage_bucket_name = 'fruit-store'
        self.aws_querystring_auth = False