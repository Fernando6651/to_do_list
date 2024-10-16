import os

# Configurações do Flask
SECRET_KEY = os.urandom(24)

# Configurações do MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'sua_senha'  # Alterar para sua senha real
MYSQL_DB = 'todo_app'

# Configuração do Flask-Login
SESSION_TYPE = 'filesystem'


