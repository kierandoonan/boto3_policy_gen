import boto3
import json
from botocore.stub import Stubber
from policy_gen.boto3 import BotoPolicyGen


class TestPolicyGen:

    def setUp(self):
        session = boto3.Session(region_name='eu-west-1')
        self.ec2 = session.client('ec2')
        self.ec2_stubber = Stubber(self.ec2)

    def tearDown(self):
        self.ec2 = None
        self.ec2_stubber = None

    def test_records_and_generates_policy(self):
        self.ec2_stubber.add_response('describe_instances', {}, {})
        self.ec2_stubber.activate()

        policy_gen = BotoPolicyGen()
        policy_gen.record()
        self.ec2.describe_instances()
        policy = json.loads(policy_gen.generate())

        assert 'Statement' in policy
        assert len(policy['Statement']) == 1
        assert len(policy['Statement'][0]['Action']) == 1
        assert policy['Statement'][0]['Action'] == 'ec2:DescribeInstances'