import psycopg2
import argparse
import boto3
from boto3.session import Session



# For auto-geneation of the usage of program and consol o/p
def args():
        parser = argparse.ArgumentParser()
        parser.add_argument("-t",help="table to dump/recover from S3", type=int)
        parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],help="increase output verbosity")
        parser.add_argument("-s",help="database server to connect to" )
        parser.add_argument("-d",help="database name ")
        parser.add_argument("-p",help="port to connect")
        parser.add_argument("-u",help="database user to connect to" )
        parser.add_argument("-b",help="s3 bucket to connect to ")
        parser.add_argument("-f",help="file with table names")
        args = parser.parse_args()
        print(args.d)
        print(args.u)
        print(args.s)
# To connect to the database
        try:
                conn = psycopg2.connect("dbname="+ args.d + " user="+ args.u + " host="+ args.s )
                print "Success"
        except:
                print "I am unable to connect to the database"
                print(args.d)




aws_access_key_id = 'nah'
aws_secret_access_key = 'nah'

session = Session(aws_access_key_id='Nah...',aws_secret_access_key='Nah..')

# This snippet below is for listing buckets

#s3 = session.resource('s3')
#my_bucket = s3.Bucket('buc1y')
#for file in my_bucket.objects.all():
#        print file.key


# This snippet will create a bucket .
#s3 = session.resource('s3')
#s3.create_bucket(Bucket='myb0054l')

def Main():
        args()
        print("IN MAIN")


if __name__=='__main__':
        Main()
