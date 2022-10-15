resource "aws_s3_bucket" "website_bucket" {
  bucket = "plateupseeds-${var.environment}-${local.account_number}"
  acl    = "public-read"

  website {
    index_document = "index.html"
  }
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_policy" "allow_access_from_public" {
  bucket = aws_s3_bucket.website_bucket.id
  policy = data.aws_iam_policy_document.allow_access_from_public.json
}

data "aws_iam_policy_document" "allow_access_from_public" {
  statement {
    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.website_bucket.arn,
      "${aws_s3_bucket.website_bucket.arn}/*",
    ]
  }
}


resource "aws_cloudfront_distribution" "s3_distribution" {
  aliases = var.cf_aliases

  default_root_object = "index.html"

  origin {
    domain_name = aws_s3_bucket.website_bucket.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
  }

  origin {
    domain_name = aws_lb.plateupseedsapi.dns_name
    origin_id   = local.lb_origin_id
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "match-viewer"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.lb_origin_id

    forwarded_values {
      query_string = true

      cookies {
        forward = "none"
      }
      headers = ["*"]
    }

    viewer_protocol_policy = "allow-all"
  }

  ordered_cache_behavior {
    path_pattern     = "assets/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "allow-all"
    compress               = true

    default_ttl = 86400
  }

  ordered_cache_behavior {
    path_pattern     = "privacy/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "allow-all"
    compress               = true

    default_ttl = 86400
  }

  ordered_cache_behavior {
    path_pattern     = "favicon.ico"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "allow-all"
    compress               = true


    default_ttl = 86400
  }

  ordered_cache_behavior {
    path_pattern     = "index.html"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "allow-all"
    compress               = true


    default_ttl = 86400
  }

  enabled         = true
  is_ipv6_enabled = true

  viewer_certificate {
    acm_certificate_arn = local.acm_certificate_arn
    ssl_support_method  = "sni-only"
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

resource "aws_ecs_cluster" "cluster" {
  name = "${var.environment}-plateupseeds"
}

resource "aws_security_group" "plateupseedsapi_loadbalancer" {
  name        = "${var.environment}-plateupseedsapi-loadbalancer"
  description = "Allow inbound traffic from the internet"
  vpc_id      = local.vpc_id

  ingress {
    description = "Allow inbound traffic from the internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow inbound traffic from the internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "plateupseedsapi" {
  name               = "${var.environment}-plateupseedsapi"
  load_balancer_type = "application"
  security_groups    = [aws_security_group.plateupseedsapi_loadbalancer.id]
  subnets            = local.public_subnets
}

resource "aws_lb_target_group" "plateupseedsapi" {
  name        = "${var.environment}-plateupseedsapi"
  target_type = "ip"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = local.vpc_id

  health_check {
    path = "/db_health"
  }
}

resource "aws_lb_listener" "plateupseedsapi443" {
  load_balancer_arn = aws_lb.plateupseedsapi.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = local.acm_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.plateupseedsapi.arn
  }
}

resource "aws_lb_listener" "plateupseedsapi80" {
  load_balancer_arn = aws_lb.plateupseedsapi.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.plateupseedsapi.arn
  }
}

resource "aws_cloudwatch_log_group" "plateupseedsapi" {
  name = "/${var.environment}/ecs/plateupseedsapi"
}

resource "aws_ecs_task_definition" "plateupseedsapi" {
  family                   = "${var.environment}-plateupseedsapi"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = local.task_execution_role
  container_definitions = jsonencode([
    {
      name      = "plateupseedsapi"
      image     = "dingxuanyao/plateupseeds:v1"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment = [
        { "name" : "TOOD", "value" : "TODO2" },
        { "name" : "ENV_FILE", "value" : ".env.${var.environment}" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.plateupseedsapi.name
          "awslogs-region"        = local.region
          "awslogs-stream-prefix" = "plateupseedsapi"
        }
      }
    }
  ])
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}

resource "aws_security_group" "plateupseedsapi_task" {
  name        = "${var.environment}-plateupseedsapi-task"
  description = "Allow inbound traffic from the load balancer"
  vpc_id      = local.vpc_id

  ingress {
    description     = "Allow inbound traffic from the load balancer"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.plateupseedsapi_loadbalancer.id]
  }

  ingress {
    description     = "Allow inbound traffic from the load balancer"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.plateupseedsapi_loadbalancer.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "plateupseedsapi" {
  name            = "${var.environment}-plateupseedsapi"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.plateupseedsapi.arn
  desired_count   = var.desired_task_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.plateupseedsapi.arn
    container_name   = "plateupseedsapi"
    container_port   = 80
  }
  network_configuration {
    subnets          = local.public_subnets
    security_groups  = [aws_security_group.plateupseedsapi_task.id]
    assign_public_ip = true
  }
}

resource "aws_db_subnet_group" "plateupseedsapi" {
  name       = "${var.environment}-plateupseedsapi"
  subnet_ids = local.private_subnets
}

resource "aws_security_group" "plateupseedsapi_database" {
  name        = "${var.environment}-plateupseedsapi-database"
  description = "Allow inbound traffic from the load balancer"
  vpc_id      = local.vpc_id

  ingress {
    description     = "Allow inbound traffic from app"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.plateupseedsapi_task.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "random_password" "plateupseedsapi_db_rw" {
  length  = 16
  special = false
}

resource "aws_db_instance" "plateupseedsapi" {
  identifier                      = "${var.environment}-plateupseedsapi"
  engine                          = "postgres"
  engine_version                  = "14.4"
  instance_class                  = "db.t4g.micro"
  allocated_storage               = 20
  username                        = "plateupseedsapi_db_rw"
  password                        = random_password.plateupseedsapi_db_rw.result
  vpc_security_group_ids          = [aws_security_group.plateupseedsapi_database.id]
  db_subnet_group_name            = aws_db_subnet_group.plateupseedsapi.name
  skip_final_snapshot             = true
  publicly_accessible             = false
  deletion_protection             = false
  apply_immediately               = true
  backup_retention_period         = 0
  storage_encrypted               = true
  auto_minor_version_upgrade      = true
  monitoring_interval             = 0
  multi_az                        = false
  copy_tags_to_snapshot           = false
  monitoring_role_arn             = ""
  performance_insights_enabled    = false
  performance_insights_kms_key_id = ""
  storage_type                    = "gp2"
  max_allocated_storage           = 0
  enabled_cloudwatch_logs_exports = []
  tags = {
    Name = "${var.environment}-plateupseedsapi"
  }
}
