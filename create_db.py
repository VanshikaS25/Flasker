import mysql.connector

mydb = mysql.connector.connect(
	user='root', 
	password='asdfghjkl', 
	host='localhost',
	auth_plugin='mysql_native_password'
	)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE IF NOT EXISTS flask_users")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
	print(db)

