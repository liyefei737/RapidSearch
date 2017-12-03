#AWS deployment script
import boto.ec2

ACCESSKEY = "XXXX"
SECRETACCESSKEY = "XXXXX"

ec2 = boto.ec2.connect_to_region("us-east-1", aws_access_key_id=ACCESSKEY,aws_secret_access_key=SECRETACCESSKEY)
keypair_us_east_1 = ec2.create_key_pair("keypair-us-east-1")

#save the keypair's .pem file in the current directory
keypair_us_east_1.save(".")

security_group = ec2.create_security_group("us-east-1","us-east-1")

# ubuntu image
new_instances = ec2.run_instances("ami-8caa1ce4") 

