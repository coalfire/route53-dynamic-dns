Route53 Dynamic DNS
===================

A daemon to update AWS Route53 private hosted zone DNS records.

The primary intent of this is to be able to have two VPN servers in different
availability zones, providing high availability, but still be able to reach
the VPN clients no matter which VPN endpoint they attach to.

Here are some nice implementations that didn't do quite what I wanted:

* https://willwarren.com/2014/07/03/roll-dynamic-dns-service-using-amazon-route53/
* https://aws.amazon.com/blogs/compute/building-a-dynamic-dns-for-route-53-using-cloudwatch-events-and-lambda/
* https://github.com/awslabs/route53-dynamic-dns-with-lambda

TODO
====

* Drop privileges.
* pip package
* documentation
* timestamp logs

License
-------
This project is licensed under the terms of the MIT license.
