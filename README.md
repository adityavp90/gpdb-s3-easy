-- Commands --
To Dump Table to S3: 
./gp-s3easy.py --dump -d gpadmin -u gpadmin -s localhost -c /path/to/greenplum/s3/s3.conf -b aws_bucket -t table_to_dump

To Restore Table from S3: 
./gp-s3easy.py --restore -d gpadmin -u gpadmin -s localhost -c /path/to/greenplum/s3/s3.conf -b aws_bucket -t table_to_dump
