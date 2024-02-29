terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "5.37.0"
    }
  }
}

provider "aws" {
  region = var.aws_region != "" ? var.aws_region : "${var.aws_region}"
}

variable "aws_region" {
    description = "AWS region for all resources."

    type = string
    default = "eu-west-1"
}

variable "master_username" {
  default = ""
}

variable "master_password" {
  default = ""
}