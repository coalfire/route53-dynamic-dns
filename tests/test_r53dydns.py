import unittest
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import r53dydns

class ChangeTest(unittest.TestCase):

    def setUp(self):
        self.fqdn = "fqdn.example.com"
        self.ip = ["203.0.113.0.128"]

    def testChange(self):

        expected = {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": self.fqdn,
                "Type": "A",
                "TTL": 180,
                "ResourceRecords": [
                    {
                        "Value": self.ip
                    },
                ],
            }
        }
        result = r53dydns.change(self.fqdn, self.ip)
        self.assertEqual(expected, result)

class ChangeBatchTest(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.comment = "something to say about this record set"
        self.fqdn1 = "fqdn1.example.com"
        self.ip1 = ["203.0.113.0.128"]
        self.change1 = r53dydns.change(self.fqdn1, self.ip1)

        self.fqdn2 = "fqdn2.example.com"
        self.ip2 = ["203.0.113.0.129"]
        self.change2 = r53dydns.change(self.fqdn2, self.ip2)

    def testChangeBatch1Change(self):

        expected= {
            "Comment": self.comment,
            "Changes": [ self.change1 ],
        }
        result = r53dydns.change_batch([self.change1], comment=self.comment)
        self.assertEqual(expected, result)

    def testChangeBatch2Changes(self):

        expected= {
            "Comment": self.comment,
            "Changes": [ self.change1, self.change2 ],
        }
        result = r53dydns.change_batch([self.change1, self.change2], comment=self.comment)
        self.assertEqual(expected, result)

        
class RequestChangeRecordSetTest(unittest.TestCase):

    def setup(self):
        self.comment = "something to say about this record set"
        self.fqdn = "fqdn1.example.com"
        self.ip = ["203.0.113.0.128"]
        self.change = r53dydns.change(self.fqdn, self.ip)
        self.change_batch = r53dydns.change_batch([self.change], self.comment)

    @unittest.skip("http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html")
    def testRequestChangeRecordSetTimeout(self):
        self.assertTrue(False)

    @unittest.skip("http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html")
    def testRequestChangeRecordSetExceedLimit(self):
        self.assertTrue(False)

    @unittest.skip("needs a mock")
    def testRequestChangeRecordSetBadDomain(self):
        self.assertTrue(False)

    @unittest.skip("needs a mock")
    def testRequestChangeRecordSet(self):
        self.assertTrue(False)

    """
    {
        'ResponseMetadata': {
            'RequestId': '59c0ede0-5777-11e7-9022-754133890b2c',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'x-amzn-requestid': '59c0ede0-5777-11e7-9022-754133890b2c',
                'content-type': 'text/xml',
                'content-length': '319',
                'date': 'Thu, 22 Jun 2017 18:19:36 GMT'
                },
            'RetryAttempts': 0
        },
        'ChangeInfo': {
            'Id': '/change/C2S3034EJ8IQRK',
            'Status': 'PENDING',
            'SubmittedAt': datetime.datetime(2017, 6, 22, 18, 19, 37, 697000, tzinfo=tzutc()),
            'Comment': 'created by route53-dydns'
        }
    }
    """

if __name__ == '__main__':
    unittest.main()
