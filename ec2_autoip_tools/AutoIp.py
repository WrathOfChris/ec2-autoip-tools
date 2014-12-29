import boto
import boto.ec2
import boto.ec2.autoscale
import boto.utils

class AutoIpInstance():
    """
    AutoIp
    """

    def __init__(self, region):
        self.region = region
        self.ec2 = boto.ec2.connect_to_region(self.region)
        self.asg = boto.ec2.autoscale.connect_to_region(self.region)
        self.info = dict()
        self.get_instance_info()
        self.get_instance_addrs()
        self.get_instance_tags()

    def get(self):
        self.info['tags'] = list()
        for tag in self.tags:
            self.info['tags'].append({str(tag.name): str(tag.value)})
        return self.info

    def get_instance_info(self):
        identity = boto.utils.get_instance_identity(timeout=60,
                num_retries=5)
        self.info['instanceId'] = str(identity['document'][u'instanceId'])
        self.info['availabilityZone'] = str(identity['document'][u'availabilityZone'])
        self.info['region'] = str(identity['document'][u'region'])
        return self.info

    def get_instance_addrs(self):
        addrfilter = { 'instance-id': self.info['instanceId'] }
        self.addrs = self.ec2.get_all_addresses(filters=addrfilter)
        return self.addrs

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
