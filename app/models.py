from flask_login import UserMixin
from flask_mysqldb import MySQL

mysql = MySQL()



class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get_user_by_id(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None

    @staticmethod
    def get_user_by_username(username):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None

    @staticmethod
    def update_profile(user_id, username, password):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", (username, password, user_id))
        mysql.connection.commit()
        cursor.close()

class Task:
    @staticmethod
    def get_tasks_by_user(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks

    @staticmethod
    def create_task(description, user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO tasks (description, user_id, completed) VALUES (%s, %s, %s)", (description, user_id, False))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def delete_task(task_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def toggle_task_completion(task_id):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE tasks SET completed = NOT completed WHERE id = %s", (task_id,))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_paginated_tasks_by_user(user_id, page, per_page):
        cursor = mysql.connection.cursor()
        offset = (page - 1) * per_page
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s LIMIT %s OFFSET %s", (user_id, per_page, offset))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks

    @staticmethod
    def search_tasks_by_user(user_id, search, page, per_page):
        cursor = mysql.connection.cursor()
        offset = (page - 1) * per_page
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s AND description LIKE %s LIMIT %s OFFSET %s", 
                        (user_id, '%' + search + '%', per_page, offset))
        tasks = cursor.fetchall()
        cursor.close()
        return tasks

    @staticmethod
    def get_task_by_id(task_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()
        return task
