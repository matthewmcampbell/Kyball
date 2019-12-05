variable "user" {
	default = "kylexi"
}

variable "password" {
	default = "Nine9clock!"
}

provider "aws" {
	profile = "default"
	region  = "us-east-1"
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
  identifier		   = "kyball-mysql"
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