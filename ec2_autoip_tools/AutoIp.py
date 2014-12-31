import boto
import boto.ec2
import boto.ec2.autoscale
import boto.utils
import sys

class AutoIpInstance():
    """
    AutoIp
    """

    def __init__(self, region):
        self.tagname = 'elasticips'
        self.region = region
        self.ec2 = boto.ec2.connect_to_region(self.region)
        self.asg = boto.ec2.autoscale.connect_to_region(self.region)
        self.info = dict()
        self.desiredips = list()
        self.desiredinfo = list()
        self.get_instance_info()
        self.get_instance_addrs()
        self.get_instance_tags()
        self.get_desired_ips()

    def get(self):
        self.info['tags'] = dict()
        for tag in self.tags:
            self.info['tags'][str(tag.name)] = str(tag.value)
        return self.info

    def get_instance_info(self):
        identity = boto.utils.get_instance_identity(timeout=60,
                num_retries=5)
        self.info['instanceId'] = str(identity['document'][u'instanceId'])
        self.info['availabilityZone'] = str(
                identity['document'][u'availabilityZone'])
        self.info['region'] = str(identity['document'][u'region'])
        return self.info

    def get_instance_addrs(self):
        addrfilter = { 'instance-id': self.info['instanceId'] }
        addrs = self.ec2.get_all_addresses(filters=addrfilter)
        self.info['addrs'] = list()
        for addr in addrs:
            self.info['addrs'].append(str(addr.public_ip))
        return self.info['addrs']

    def get_instance_tags(self):
        tagsfilter = { 'resource-id': self.info['instanceId'] }
        self.tags = self.ec2.get_all_tags(tagsfilter)
        return self.tags

    def find_instance_tag(self, key):
        for tag in self.tags:
            if str(tag.name) == str(key):
                return tag
        return None

    def get_autoscale_group(self):
        asgtag = self.find_instance_tag('aws:autoscaling:groupName')
        if not asgtag:
            return None
        return str(asgtag.value)

    def get_desired_ips(self):
        tag = self.find_instance_tag(self.tagname)
        if not tag:
            return None
        self.desiredips = str(tag.value).split()
        if len(self.desiredips) > 0:
            self.desiredinfo = self.ec2.get_all_addresses(
                    addresses=self.desiredips)
        return self.desiredips

    def get_candidate_ips(self):
        candidates = list()
        for addr in self.desiredinfo:
            if addr.association_id == None:
                candidates.append(str(addr.public_ip))
        return candidates

    def find_desired_info(self, key):
        for addr in self.desiredinfo:
            if str(addr.public_ip) == str(key):
                return addr
        return None

    def associate_address(self, addr):
        info = self.find_desired_info(addr)
        if not info:
            return False
        try:
            self.ec2.associate_address(
                    self.info['instanceId'],
                    allocation_id = info.allocation_id,
                    allow_reassociation=False
                    )
        except boto.exception.BotoServerError as e:
            sys.stderr.write("Cannot associate address %s\n" % addr)
            sys.stderr.write("Error: %s\n" % e)
            return False

        return True
