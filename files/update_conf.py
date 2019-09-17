#!/usr/bin/env python

import os
import sys
from ec2_metadata import ec2_metadata
import ConfigParser

if ec2_metadata.private_ipv4:
    Host_IPAddr = ec2_metadata.private_ipv4
elif os.environ['RESULTSERVER_IP']:
    Host_IPAddr = os.environ['RESULTSERVER_IP']
else:
    Host_IPAddr = ""

# Setting reporting.conf
reporting_cfg = ConfigParser.ConfigParser()
reporting_cfg.read(".cuckoo/conf/reporting.conf")
with open(".cuckoo/conf/reporting.conf", 'w') as cfile:
    if os.environ.get('ES_HOST'):
        reporting_cfg.set('elasticsearch', 'enabled', "yes")
        if os.environ.get('ES_PORT'):
            reporting_cfg.set('elasticsearch', 'hosts', "%s:%s" % (os.environ['ES_HOST'], os.environ['ES_PORT']))
        else:
            reporting_cfg.set('elasticsearch', 'hosts', os.environ['ES_HOST'])
    if os.environ.get('MONGO_HOST'):
        reporting_cfg.set('mongodb', 'enabled', "yes")
        reporting_cfg.set('mongodb', 'host', os.environ['MONGO_HOST'])
    if os.environ.get('MONGO_TCP_PORT'):
        reporting_cfg.set('mongodb', 'port', os.environ['MONGO_TCP_PORT'])
    if os.environ.get('MONGO_DATABASE'):
        reporting_cfg.set('mongodb', 'db', os.environ['MONGO_DATABASE'])
    if os.environ.get('MONGO_USER'):
        reporting_cfg.set('mongodb', 'username', os.environ['MONGO_USER'])
    if os.environ.get('MONGO_PASSWORD'):
        reporting_cfg.set('mongodb', 'password', os.environ['MONGO_PASSWORD'])

    reporting_cfg.write(cfile)

# Setting cuckoo.conf
cuckoo_cfg = ConfigParser.ConfigParser()
cuckoo_cfg.read(".cuckoo/conf/cuckoo.conf")
with open(".cuckoo/conf/cuckoo.conf", 'w') as cfile:
    if Host_IPAddr:
        cuckoo_cfg.set('resultserver', 'ip', '0.0.0.0')
    if os.environ.get('RESULTSERVER_PORT'):
        cuckoo_cfg.set('resultserver', 'port', os.environ['RESULTSERVER_PORT'])
    if os.environ.get('MACHINERY'):
        cuckoo_cfg.set('cuckoo', 'machinery', os.environ['MACHINERY'])
    if os.environ.get('POSTGRES_HOST'):
        cuckoo_cfg.set(
            'database',
            'connection',
            "postgresql://%s:%s@%s:%s/%s" % (
            os.environ['POSTGRES_USER'], os.environ['POSTGRES_PASSWORD'], os.environ['POSTGRES_HOST'],
            os.environ['POSTGRES_TCP_PORT'], os.environ['POSTGRES_DATABASE']))
    if os.environ.get('VBOX_IGNORE_VULNERABILITIES'):
        cuckoo_cfg.set('cuckoo', 'ignore_vulnerabilities', os.environ['VBOX_IGNORE_VULNERABILITIES'])
    if os.environ.get('API_TOKEN'):
        cuckoo_cfg.set('cuckoo', 'api_token', os.environ['API_TOKEN'])
    cuckoo_cfg.set('timeouts', 'vm_state', 900)
    cuckoo_cfg.write(cfile)

# Setting aws.conf
aws_cfg = ConfigParser.ConfigParser()
aws_cfg.read(".cuckoo/conf/aws.conf")
with open(".cuckoo/conf/aws.conf", 'w') as cfile:
    if os.environ.get('AWS_REGION'):
        aws_cfg.set('aws', 'region_name', os.environ['AWS_REGION'])
    if os.environ.get('RUNNING_MACHINES_GAP'):
        aws_cfg.set('aws', 'running_machines_gap', os.environ['RUNNING_MACHINES_GAP'])
    if os.environ.get('GUEST_AMI_ID'):
        aws_cfg.set('autoscale', 'image_id', os.environ['GUEST_AMI_ID'])
    if os.environ.get('AWS_SUBNET_GUEST'):
        aws_cfg.set('autoscale', 'subnet_id', os.environ['AWS_SUBNET_GUEST'])
    if os.environ.get('AWS_SECURITY_GROUP_GUEST'):
        aws_cfg.set('autoscale', 'security_groups', os.environ['AWS_SECURITY_GROUP_GUEST'])
    if os.environ.get('GUEST_INSTANCE_TYPE'):
        aws_cfg.set('autoscale', 'instance_type', os.environ['GUEST_INSTANCE_TYPE'])
    aws_cfg.set('autoscale', 'autoscale', 'yes')
    if os.environ.get('GUEST_INSTANCE_TYPE'):
        aws_cfg.set('autoscale', 'instance_type', os.environ['GUEST_INSTANCE_TYPE'])
    aws_cfg.set('autoscale', 'resultserver_ip', Host_IPAddr)
    if os.environ.get('RESULTSERVER_PORT'):
        aws_cfg.set('autoscale', 'resultserver_port', os.environ['RESULTSERVER_PORT'])

    aws_cfg.write(cfile)

# Setting processing.conf
processing_cfg = ConfigParser.ConfigParser()
processing_cfg.read(".cuckoo/conf/processing.conf")
with open(".cuckoo/conf/processing.conf", 'w') as cfile:
    if os.environ.get('ALLOWED_DNS'):
        processing_cfg.set('network', 'whitelist_dns', 'yes')
        processing_cfg.set('network', 'allowed_dns', os.environ['ALLOWED_DNS'])

    if os.environ.get('EXTRACT_DLL'):
        processing_cfg.set('procmemory', 'extract_dll', os.environ['EXTRACT_DLL'])

    if os.environ.get('ENABLE_STRINGS'):
        processing_cfg.set('strings', 'enabled', os.environ['ENABLE_STRINGS'])

    if os.environ.get('ENABLE_SURICATA'):
        processing_cfg.set('suricata', 'enabled', os.environ['ENABLE_SURICATA'])

    if os.environ.get('ENABLE_VIRUSTOTAL'):
        processing_cfg.set('virustotal', 'enabled', os.environ['ENABLE_VIRUSTOTAL'])

    processing_cfg.write(cfile)

# Setting auxiliary.conf
auxiliary_cfg = ConfigParser.ConfigParser()
auxiliary_cfg.read(".cuckoo/conf/auxiliary.conf")
with open(".cuckoo/conf/auxiliary.conf", 'w') as cfile:
    if os.environ.get('ENABLE_MITM'):
        auxiliary_cfg.set('mitm', 'enabled', os.environ['ENABLE_MITM'])

    auxiliary_cfg.write(cfile)

sys.exit()
