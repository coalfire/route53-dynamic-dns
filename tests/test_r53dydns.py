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

class RecordSetTest(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        self.comment = "something to say about this record set"
        self.fqdn1 = "fqdn1.example.com"
        self.ip1 = ["203.0.113.0.128"]
        self.change1 = r53dydns.change(self.fqdn1, self.ip1)

        self.fqdn2 = "fqdn2.example.com"
        self.ip2 = ["203.0.113.0.129"]
        self.change2 = r53dydns.change(self.fqdn2, self.ip2)

    def testRecordSet1Change(self):

        expected= {
            "Comment": self.comment,
            "Changes": [ self.change1 ],
        }
        result = r53dydns.record_set([self.change1], comment=self.comment)
        self.assertEqual(expected, result)

        
if __name__ == '__main__':
    unittest.main()
