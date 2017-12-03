import boto.ec2
import time
import subprocess
import sys, os

def deploy():
    try:
        cred_file = open("credentials.csv", "r")
        cred_info = cred_file.readlines()[1].split(",")
        ACCESSKEY = cred_info[2]
        SECRETACCESSKEY = cred_info[3]
    except:
        print "Make sure you have credentials.csv in your current directory and the file has permission to be read."
        return

    ec2 = boto.ec2.connect_to_region("us-east-1", 
                                    aws_access_key_id=ACCESSKEY,
                                    aws_secret_access_key=SECRETACCESSKEY)
    
    # create a new keypair with name specified by key_pair_name
    # store the pem file in the current directory
    key_pair_name = "keypair21"
    ec2.create_key_pair(key_pair_name).save(".")
    os.system("chmod 400 %s.pem"%key_pair_name)
    
    # create a new security group with name specified by sec_group_name
    # store the pem file in the current directory
    sec_group_name = "group20"
    sec_group_descp = "group name: %s"%sec_group_name
    sec_group = ec2.create_security_group(sec_group_name, sec_group_descp)

    #enable PING, SSH, HTTP
    sec_group.authorize('ICMP', -1, -1, '0.0.0.0/0')
    sec_group.authorize('TCP', 22, 22, '0.0.0.0/0')
    sec_group.authorize('TCP', 80, 80, '0.0.0.0/0')
    sec_group.authorize('TCP', 8085, 8085, '0.0.0.0/0')

    # run instance
    instance = ec2.run_instances(image_id='ami-8caa1ce4', key_name=key_pair_name,
                                 security_groups=[sec_group_name], 
                                 instance_type='t1.micro').instances[0]

    while instance.update() != 'running':
    	time.sleep(3)
    
    print "instance %s is now running on %s."%(instance.id, instance.ip_address)
    instance_id = instance.id
    address = instance.ip_address
    
    time.sleep(60)

    subprocess.call("scp -i %s.pem -o StrictHostKeyChecking=no deployment_env_setup.sh ubuntu@%s:~/" % (key_pair_name, address), shell=True)
    subprocess.Popen(("ssh -i %s.pem ubuntu@%s /bin/bash ~/deployment_env_setup.sh" % (key_pair_name, address)).split())
    
    print "Search engine instance %s is running at %s/8085" %(instance_id, address)
    time.sleep(1200)
    return ("%s/8085"%address,instance_id)

if __name__ == "__main__":
    deploy()
