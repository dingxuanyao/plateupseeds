locals {
  account_number      = 939326176859
  region              = "us-east-1"
  domain_name         = "plateupseeds.com"
  s3_origin_id        = "S3-plateupseeds"
  lb_origin_id        = "LB-plateupseeds"
  acm_certificate_arn = "arn:aws:acm:us-east-1:939326176859:certificate/75fe910f-7105-4955-a3c6-c945cba16771"
  vpc_id              = "vpc-02b59f3dc07082177"
  public_subnets      = ["subnet-0205b05bc33218580", "subnet-0d9315154f5f8399f"]
  private_subnets     = ["subnet-09411c8ce98fd320f", "subnet-021ad830586b83acb"]
  task_execution_role = "arn:aws:iam::939326176859:role/TaskExecutionRole"

  common_tags = {
    environment = "production"
    app         = "plateupseeds"
  }
}
