import mysql.connector as conn
mydb = conn.connect(host="localhost", user="root", password="")
db_cursor=mydb.cursor()
db_cursor.execute('CREATE DATABASE IF NOT EXISTS `lipsync`')
db_cursor.execute('USE `lipsync`')
db_cursor.execute('CREATE TABLE IF NOT EXISTS `lipsync`.`userregdetails` (`uid` INT NOT NULL AUTO_INCREMENT , `u_fname` TEXT NOT NULL , `u_lname` TEXT NOT NULL , `u_mail` VARCHAR(90) NOT NULL , `u_pass` VARCHAR(16) NOT NULL , `u_reg_datetime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`uid`))')
db_insert = "INSERT INTO `lipsync`.`userregdetails` (u_fname, u_lname, u_mail, u_pass) VALUES (%s, %s, %s, %s)"
db_cursor.execute(db_insert, ("abc", "def", "abdf@gmail.com", "1234"))
mydb.commit()
print(db_cursor.rowcount, "Record inserted")