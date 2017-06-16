#!/home/gpadmin/anaconda2/envs/gpdb-s3/bin/python
#
#
#

import psycopg2
import argparse


parser = argparse.ArgumentParser(description="Dump/Load Gpdb tables form S3")
parser.add_argument("-t",help="table to dump/recover from S3")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],help="increase output verbosity")
args = parser.parse_args()

try:
    conn = psycopg2.connect("dbname='test' user='gpadmin' host='localhost'")
except:
    print "I am unable to connect to the database"


