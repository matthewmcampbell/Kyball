# Resources for kyball project

provider "aws" {
	profile = "default"
	region  = "us-east-1"
}

variable "app_loc" {
	default = "./../../mysite"
}

variable "namespace" {
	default = "kyball"
}

variable "environment" {
	default = "dev"
}

variable "user" {
}

variable "password" {
}

resource "aws_instance" "SQL-writer" {
  ami = "ami-0c322300a1dd5dc79"
  depends_on = [aws_db_instance.Kyball_MySQL]
  instance_type = "t2.micro"
  key_name = "mmc_user1"
  security_groups = [
      aws_security_group.SSH_to_EC2.name,
      ]
  tags = {
    Name = "SQL-writer"
  }
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install git -y
    yum install python3 -y
    cd home/ec2-user
    git clone https://github.com/Kylexi/Kyball.git
    cd Kyball/Scripts
    python3 write_to_sql_from_ec2.py ${aws_db_instance.Kyball_MySQL.address} Kyball_db ${var.user} ${var.password}
    EOF
}

resource "aws_db_instance" "Kyball_MySQL" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  identifier           = "kyball-mysql"
  instance_class       = "db.t2.micro"
  name                 = "Kyball_MySQL"
  username             = var.user
  password             = var.password
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
  vpc_security_group_ids = [
      aws_security_group.EC2_to_MySQL.id,
      ]
}

resource "aws_security_group" "SSH_to_EC2" {
  name        = "SSH_to_EC2"
  description = "Allows SSH access into EC2"
  #vpc_id      = aws_vpc.main.id
  #depends_on = [aws_instance.SQL-writer]
  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    # Please restrict your ingress to only necessary IPs and ports.
    # Opening to 0.0.0.0/0 can lead to security vulnerabilities.
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
    # prefix_list_ids = ["pl-12c4e678"]
  }
}

resource "aws_security_group" "EC2_to_MySQL" {
  name        = "EC2_to_MySQL"
  description = "Allows EC2 to access MySQL RDS"
  #vpc_id      = aws_vpc.main.id
  #depends_on = [aws_db_instance.Kyball_MySQL]
  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    # Please restrict your ingress to only necessary IPs and ports.
    # Opening to 0.0.0.0/0 can lead to security vulnerabilities.
    # cidr_blocks = 0.0.0.0/0
    security_groups = [
      aws_security_group.SSH_to_EC2.id,
      ]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
    # prefix_list_ids = ["pl-12c4e678"]
  }
}

resource "null_resource" "delay_zero" {
  provisioner "local-exec" {
    command = join(" ",["python write_mysql_name.py", aws_db_instance.Kyball_MySQL.address, var.user, var.password])
  }
  depends_on = [aws_db_instance.Kyball_MySQL]
#  triggers = {
#    "before" = "${null_resource.before.id}"
#  }
}


### ELASTIC BEANSTALK HALF ###

# create a zip of your deployment with terraform
data "archive_file" "django_zip" {
  type        = "zip"
  source_dir  = var.app_loc
  output_path = join("", [var.app_loc, ".zip"])

  depends_on = [null_resource.delay_two]
}

resource "aws_s3_bucket" "dist_bucket" {
  bucket = join("", [var.namespace, "-elb-dist"])
  acl    = "private"
}

resource "aws_s3_bucket_object" "dist_item" {
  key    = join("", [var.environment, "/dist", uuid()])
  bucket = aws_s3_bucket.dist_bucket.id
  source = data.archive_file.django_zip.output_path

  depends_on = [aws_elastic_beanstalk_environment.kyball_env]
}

resource "aws_elastic_beanstalk_application" "kyball_app" {
  name        = "kyball"
  description = "eb application instance for kyball"

  appversion_lifecycle {
    service_role          = aws_iam_service_linked_role.elastic_beanstalk_role.arn
    max_count             = 128
    delete_source_from_s3 = true
  }
}

resource "aws_elastic_beanstalk_application_version" "default" {
  name         = "ky_version"
  application  = aws_elastic_beanstalk_application.kyball_app.name
  description  = "application version created for kyball"
  bucket       = aws_s3_bucket.dist_bucket.id
  key          = aws_s3_bucket_object.dist_item.id
  force_delete = true
}

resource "aws_elastic_beanstalk_environment" "kyball_env" {
  name                = "kyball-env"
  application         = aws_elastic_beanstalk_application.kyball_app.name
  solution_stack_name = "64bit Amazon Linux 2018.03 v2.9.4 running Python 3.6"

  depends_on          = [null_resource.delay_one]
}

resource "aws_iam_service_linked_role" "elastic_beanstalk_role" {
  aws_service_name = "elasticbeanstalk.amazonaws.com"
}


resource "null_resource" "delay_one" {
  provisioner "local-exec" {
#    command = "ping -n 60 127.0.0.1 >NUL"
  	command = "python sleep.py"
  }
  depends_on = [aws_iam_service_linked_role.elastic_beanstalk_role]
#  triggers = {
#    "before" = "${null_resource.before.id}"
#  }
}

resource "null_resource" "delay_two" {
  provisioner "local-exec" {
#    command = "ping -n 60 127.0.0.1 >NUL"
  	command = join(" ",["python write_django_config_ALLOWED_HOST.py", aws_elastic_beanstalk_environment.kyball_env.cname])
  }
  depends_on = [aws_elastic_beanstalk_environment.kyball_env]
#  triggers = {
#    "before" = "${null_resource.before.id}"
#  }
}

output "app_version" {
  value = aws_elastic_beanstalk_application_version.default.name
}
output "env_name" {
  value = aws_elastic_beanstalk_environment.kyball_env.name
}