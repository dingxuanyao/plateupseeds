variable "environment" {
  type        = string
  description = "environment name"
}

variable "cf_aliases" {
  type        = list(string)
  description = "list of cloudfront aliases"
}

variable "desired_task_count" {
  type        = number
  description = "number of tasks to run"
  default     = 1
}
