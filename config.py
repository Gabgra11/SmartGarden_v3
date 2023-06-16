import os

client_id = os.environ.get("client_id")
client_secret = os.environ.get('client_secret')
login_uri = os.environ.get("login_uri")
db_name = "postgres"
db_user = "postgres"
db_password = os.environ.get("db_password")