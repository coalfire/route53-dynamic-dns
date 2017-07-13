# ROUTE53

resource "aws_route53_zone" "example-com" {
  name   = "example.com."
}

data "aws_route53_zone" "example-com" {
  name         = "example.com"
  private_zone = true
}

output "example-com-zone-id" {
  value = "${aws_route53_zone.example-com.zone_id}"
}

# IAM 

data "aws_iam_policy_document" "assume-role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "update-example-com-records" {
  name = "update-example-com-records"
  description = "Allow EC2 instances to update example.com records"
  path               = "/"
  assume_role_policy = "${data.aws_iam_policy_document.assume-role.json}"
}

data "aws_iam_policy_document" "update-example-com-records" {
  statement {
    actions = [
      "route53:ChangeResourceRecordSets"
    ]
    resources = [
      "arn:aws:route53:::hostedzone/${aws_route53_zone.example-com.zone_id}"
    ]
  }
}

resource "aws_iam_policy" "update-example-com-records" {
  name = "update-example-com-records"
  description = "update example.com private hosted zone records"
  policy = "${data.aws_iam_policy_document.update-example-com-records.json}"
}

resource "aws_iam_role_policy_attachment" "update-example-com-records" {
  role = "${aws_iam_role.update-example-com-records.name}"
  policy_arn = "${aws_iam_policy.update-example-com-records.arn}"
}

resource "aws_iam_instance_profile" "update-example-com-records" {
  name = "update-example-com-records"
  role = "${aws_iam_role.update-example-com-records.name}"
}

resource "aws_iam_policy_attachment" "update-example-com-records" {
  name = "update-example-com-records"
  roles = [ "${aws_iam_role.update-example-com-records.name}" ]
  policy_arn = "${aws_iam_policy.update-example-com-records.arn}"
}

# EC2

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "my-vpn-01" {
  ami           = "ami-ae7bfdb8"      #centos7
  instance_type = "t2.micro"
  associate_public_ip_address = true
  source_dest_check           = false

  iam_instance_profile = "${aws_iam_instance_profile.update-example-com-records.name}"

  tags {
    Name  = "my-vpn-01"
  }
}

