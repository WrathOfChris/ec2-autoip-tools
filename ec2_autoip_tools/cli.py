import argparse
import json
import yaml
from .util import common_parser, common_args, catch_sigint
from .AutoIp import AutoIpInstance

#import boto.utils
#from netaddr import IPNetwork, AddrFormatError, AddrConversionError
# identity = boto.utils.get_instance_identity()

def ec2_autoip_list():
    catch_sigint()
    parser = common_parser('AutoIP list')
    args = parser.parse_args()
    common_args(args)
    autoip = AutoIpInstance(args.region)
    from pprint import pprint
    info = autoip.get()
    pprint(info)

def ec2_autoip_atboot():
    catch_sigint()
    parser = common_parser('AutoIP atboot')
    args = parser.parse_args()
    common_args(args)
    print args.region
