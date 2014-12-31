ec2-autoip-tools
================

Tools for auto-assigning IP addresses within EC2

## IAM Permissions

```
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:AssociateAddress",
        "ec2:DescribeAddresses",
        "ec2:DescribeTags"
      ],
      "Resource": "*"
    }
  ]
}
```
