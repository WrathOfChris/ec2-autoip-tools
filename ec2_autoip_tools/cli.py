import argparse
import sys
import json
import yaml
from .util import common_parser, common_args, catch_sigint
from .AutoIp import AutoIpInstance

def ec2_autoip_list():
    catch_sigint()
    parser = common_parser('AutoIP list')
    parsergroup = parser.add_mutually_exclusive_group()
    parsergroup.add_argument(
            '-j',
            '--json',
            help='json output',
            action='store_true'
            )
    parsergroup.add_argument(
            '-y',
            '--yaml',
            help='yaml output',
            action='store_true'
            )
    args = parser.parse_args()
    common_args(args)
    autoip = AutoIpInstance(args.region)

    if args.json:
        print json.dumps(autoip.get_desired_ips())
    elif args.yaml:
        print yaml.dump(autoip.get_desired_ips())
    else:
        for eip in autoip.get_desired_ips():
            print eip

def ec2_autoip_atboot():
    catch_sigint()
    parser = common_parser('AutoIP atboot')
    args = parser.parse_args()
    common_args(args)

    autoip = AutoIpInstance(args.region)

    addrs = autoip.get_instance_addrs()
    if addrs and len(addrs) > 0:
        sys.stderr.write('ElasticIP already assigned, exiting\n')
        sys.exit(0)

    eips = autoip.get_candidate_ips()
    if not eips or len(eips) == 0:
        sys.stderr.write('No candidate ElasticIPs available, exiting\n')
        sys.exit(1)

    for eip in eips:
        if autoip.associate_address(eip):
            sys.stderr.write("Successfully associated address %s\n" % eip)
            sys.exit(0)

    sys.exit(1)
