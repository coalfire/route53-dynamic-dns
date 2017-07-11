resource "aws_route53_zone" "example-com" {
  name   = "example.com."
}

data "aws_route53_zone" "lighthouse-sec" {
  name         = "lighthouse.sec"
  private_zone = true
}

output "example-com-zone-id" {
  value = "${aws_route53_zone.zone_id}"
}

FIXME add IAM role
