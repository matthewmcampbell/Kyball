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
}

resource "aws_s3_bucket" "dist_bucket" {
  bucket = join("", [var.namespace, "-elb-dist"])
  acl    = "private"
}

resource "aws_s3_bucket_object" "dist_item" {
  key    = join("", [var.environment, "/dist", uuid()])
  bucket = aws_s3_bucket.dist_bucket.id
  source = data.archive_file.django_zip.output_path
}

resource "aws_elastic_beanstalk_application" "kyball_app" {
  name        = "kyball"
  description = "eb application instance for kyball"

  appversion_lifecycle {
    service_role          = aws_iam_service_linked_role.elasticbeanstalk_role.arn
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
}

resource "aws_iam_service_linked_role" "elasticbeanstalk_role" {
  aws_service_name = "elasticbeanstalk.amazonaws.com"
}

#module "elastic_beanstalk_application" {
#  source    = "git::https://github.com/cloudposse/terraform-aws-elastic-beanstalk-application.git?ref=master"
#  namespace = var.namespace
#  stage     = var.environment
#  name      = var.app
#}
#module "elastic_beanstalk_environment" {
#  source = "git::https://github.com/cloudposse/terraform-aws-elastic-beanstalk-environment.git?ref=master"
#}
#resource "aws_elastic_beanstalk_application_version" "default" {
#  name        = var.namespace-var.environment-uuid()
#  application = module.elastic_beanstalk_application.app_name
#  description = "application version created by terraform"
#  bucket      = aws_s3_bucket.dist_bucket.id
#  key         = aws_s3_bucket_object.dist_item.id
#}

output "app_version" {
  value = aws_elastic_beanstalk_application_version.default.name
}
output "env_name" {
  value = aws_elastic_beanstalk_environment.kyball_env.name
}

output "cname" {
  value = aws_elastic_beanstalk_environment.kyball_env.cname
}