#!/home/gpadmin/anaconda2/envs/gpdb-s3/bin/python

import time
import os
import psycopg2
import argparse
import boto3


def get_args(argv=None):
        parser = argparse.ArgumentParser(description="Dump/Fetch Greenplum Data to/from S3")
        parser.add_argument("-t",help="table to dump/recover from S3")
        parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],help="increase output verbosity")
        parser.add_argument("-s",help="database server to connect to" )
        parser.add_argument("-d",help="database name ")
        parser.add_argument("-p",help="port to connect")
        parser.add_argument("-u",help="database user to connect to" )
        parser.add_argument("-b",help="s3 bucket to connect to ")
        parser.add_argument("-f",help="file with table names")
        parser.add_argument("-c",help="config file for s3 credentials. User must have read/write access to S3")
	parser.add_argument("--dump", action="store_true")
	parser.add_argument("--restore", action="store_true")	
	return parser.parse_args()
	

def get_s3_conf(s3_conf_file):
	d = {}
	with open(s3_conf_file) as f:
		for line in f:
			try:
				(key, val) = line.split("=")
			except ValueError:
				continue
			d[str(key.strip())] = val.strip().strip('"')
	return d

def get_gpdb_conn(dbname,user,host):
	try:
                conn = psycopg2.connect("dbname="+ dbname + " user="+ user + " host="+ host )
                print "Connection to DB established"
		return conn
        except:
                print "Unable to connect to DB"

# Test function
def list_bucket_objects(accessid,secret,bucket):
	session = boto3.Session(aws_access_key_id=accessid,aws_secret_access_key=secret)
	s3 = session.resource('s3')
	gpdb_backup_bucket = s3.Bucket(bucket)
	for file in gpdb_backup_bucket.objects.all():
		print file.key

#Improve to include availability zone
def get_location_string(bucket,table_name,config_file):
	location="s3://s3-us-west-1.amazonaws.com/{}/{}/{}/ config={}".format(bucket,table_name,time.strftime("%m%d%Y"),config_file)
	#print location
	return location

# - Handle multiple dumps on the same day 
def dump_to_S3(conn,table_name,location):
	external_table_name="ext_"+str(args.t)+time.strftime("%m%d%Y")
	file_format="CSV"
	cur=conn.cursor()
	try:
		cur.execute("""CREATE WRITABLE EXTERNAL TABLE %s ( LIKE %s) LOCATION ('%s') FORMAT '%s'""" % (external_table_name,table_name,location,file_format))		
		conn.commit()
	except psycopg2.ProgrammingError:
		conn.rollback()
	cur.execute("""INSERT INTO %s (SELECT * FROM %s)""" % (external_table_name,table_name))
	conn.commit()	

# - Table must exist, put schema on S3?
# - Currently only restores from current date - Include date option, restore from nearest date
def restore_from_S3(conn,table_name,location):
	external_table_name="ext_"+str(args.t)
        file_format="CSV"
	cur=conn.cursor()
	try:
        	cur.execute("""CREATE READABLE EXTERNAL TABLE %s ( LIKE %s) LOCATION ('%s') FORMAT '%s'""" % (external_table_name,table_name,location,file_format))
		conn.commit()
	except psycopg2.ProgrammingError:
		conn.rollback()
	cur.execute("""INSERT INTO %s (SELECT * FROM %s)""" % (table_name,external_table_name))
	conn.commit()


if __name__=='__main__':
	argvals = None       
	args = get_args(argvals)
	s3_conf = get_s3_conf(args.c)
	conn = get_gpdb_conn(args.d,args.u,args.s)
	location = get_location_string(args.b,args.t,args.c)

	if args.dump:
		dump_to_S3(conn,args.t,location)
	elif args.restore:
		restore_from_S3(conn,args.t,location)
	else:
		print "Need argument --dump/--restore"
