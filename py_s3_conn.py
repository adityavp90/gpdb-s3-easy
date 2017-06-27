import boto3
from boto3.session import Session


aws_access_key_id = 'nah'
aws_secret_access_key = 'nah'

session = Session(aws_access_key_id='Nah...',aws_secret_access_key='Nah..')

# This snippet below is for listing buckets

s3 = session.resource('s3')
my_bucket = s3.Bucket('buc1y')
for file in my_bucket.objects.all():
        print file.key


# This snippet will create a bucket .
s3 = session.resource('s3')
s3.create_bucket(Bucket='myb0054l')
