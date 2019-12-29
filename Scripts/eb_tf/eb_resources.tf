# Resources for elastic beanstalk deployment of Django app

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