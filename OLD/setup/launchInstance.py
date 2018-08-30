#!/usr/bin/env python
import boto3

ec2 = boto3.resource('ec2', region_name='ap-southeast-2')
instances = ec2.create_instances(ImageId='ami-47c21a25', MinCount=1, MaxCount=1, 
                    DryRun=False, InstanceType='t2.medium', KeyName='ec2Admin', 
                    NetworkInterfaces=[{'SubnetId': 'subnet-fea9fcb8', 
                    'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': ['sg-ea8a7e8f']}])
instances[0].wait_until_running()
# instances[0].add_tag("Name","pdfHandler")
print(instances[0].id,'is ready')



# # list vpcs info
# for vpc in ec2.vpcs.all():
#     for subnet in vpc.subnets.all():
#         print(vpc, "all:", subnet)
#     for az in ec2.meta.client.describe_availability_zones()["AvailabilityZones"]:
#         for subnet in vpc.subnets.filter(Filters=[{"Name": "availabilityZone", "Values": [az["ZoneName"]]}]):
#             print(vpc, az["ZoneName"], "filter:", subnet)