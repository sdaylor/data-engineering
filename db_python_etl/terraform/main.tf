resource "azurerm_resource_group" "this" {
  name     = "rg-engineering-eastus2"
  location = "eastus2"
}

resource "random_string" "mysql_user" {
  length  = 8
  numeric = false
  special = false
  upper   = false
}

resource "random_password" "mysql_pass" {
  length = 16
  special = false
}

resource "azurerm_mysql_flexible_server" "this" {
  name                   = "mysql-engineering-eastus2"
  resource_group_name    = azurerm_resource_group.this.name
  location               = azurerm_resource_group.this.location
  administrator_login    = random_string.mysql_user.result
  administrator_password = random_password.mysql_pass.result
  backup_retention_days  = 7
  sku_name               = "B_Standard_B1s"
}

resource "azurerm_mysql_flexible_database" "this" {
  charset             = "utf8"
  collation           = "utf8_general_ci"
  name                = "data_engineering"
  resource_group_name = azurerm_resource_group.this.name
  server_name         = azurerm_mysql_flexible_server.this.name
}
