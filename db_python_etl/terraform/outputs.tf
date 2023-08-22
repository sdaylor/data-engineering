output "mysql_username" {
  value = random_string.mysql_user.result
  description = "Randomly generated admin username for MySQL"
  sensitive = true
}

output "mysql_password" {
  value = random_password.mysql_pass.result
  description = "Randomly generated admin password for MySQL"
  sensitive = true
}


