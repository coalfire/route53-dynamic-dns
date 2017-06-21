import unittest
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import r53dydns

class ChangeTest(unittest.TestCase):

    def setUp(self):
        self.fqdn = "fqdn.example.com"
        self.ips = ["203.0.113.0.128"]

    def testChange(self):

        expected = {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": self.fqdn,
                    "Type": "A",
                    "TTL": 180,
                    "ResourceRecords": [
                        {
                            "Value": self.ips
                        },
                    ],
                }
            }
        result = r53dydns.change(self.fqdn, self.ips)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
