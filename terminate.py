import sys
import boto.ec2

if len(sys.argv) != 2:
    print "Wrong number of arguments. Usage: python terminate.py instance_id"
    sys.exit()

instance_id = sys.argv[1]

try:
    cred_file = open("credentials.csv", "r")
    cred_info = cred_file.readlines()[1].split(",")
    ACCESSKEY = cred_info[2]
    SECRETACCESSKEY = cred_info[3]
except:
    print "Make sure you have credentials.csv in your current directory and the file has permission to be read."
    sys.exit()

ec2 = boto.ec2.connect_to_region("us-east-1", 
                                    aws_access_key_id=ACCESSKEY,
                                    aws_secret_access_key=SECRETACCESSKEY)

instances_terminated = ec2.terminate_instances(instance_id)

if (instances_terminated[0].id == instance_id):
    print "%s is terminated."%instance_id
else:
    print "%s is terminated unsuccessfully."%instance_id
