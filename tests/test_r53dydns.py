import unittest
sys.path.insert(0, os.path.abspath('..'))

import r53dydns

class ChangeTest(unittest.TestCase):

    def testChange(self):

        expected = {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": "fqdn.example.com",
                    "Type": "A",
                    "TTL": 180,
                    "ResourceRecords": [
                        {
                            "Value": "203.0.113.0.128"
                        },
                    ],
                }
            }
        result = r53dydns.change()
        self.asserEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
