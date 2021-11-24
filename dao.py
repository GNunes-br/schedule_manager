from user import User
from task import Task

SQL_CREATE_ONE = 'insert into {} value ({})'
SQL_CREATE_MANY = 'insert into {} value {}'
SQL_SELECT_ONE = 'select * from {} where {} limit 1'
SQL_SELECT_MANY = 'select * from {} where {}'
SQL_UPDATE_WHERE = 'update {} set {} where {}'
SQL_DELETE_WHERE = 'delete from {} where {}'

class UserDao:
    def __init__(self,database):
        self.__database=database

    def save(self, user):
        cursor = self.__database.connection.cursor()
        cursor.execute(SQL_CREATE_ONE.format('users (name,email,password) ','"' + user._name + '","' + user._email + '","' + user._password + '"'))
        self.__database.connection.commit()

    def findByEmail(self, email):
        cursor = self.__database.connection.cursor()
        cursor.execute(SQL_SELECT_ONE.format('users', 'email = "{}"'.format(email)))
        return cursor.fetchone()

class TaskDao:
    def __init__(self,database):
        self.__database=database

    def save(self, task, user):
        cursor = self.__database.connection.cursor()
        cursor.execute(SQL_CREATE_ONE.format('tasks (user,name,description,situation) ', str(user) + ',"' + task._name + '","' + task._description + '","' + task._situation + '"'))
        self.__database.connection.commit()

    def updateSituation(self, id, situation):
        cursor = self.__database.connection.cursor()
        cursor.execute(SQL_UPDATE_WHERE.format('tasks','situation="' + situation + '"','id=' + id))
        self.__database.connection.commit()

    def findTaskById(self, id):
        cursor = self.__database.connection.cursor()
        cursor.execute(SQL_SELECT_ONE.format('tasks', 'id="{}"'.format(id)))
        return cursor.fetchone()

    def findTasks(self,user):
        cursor = self.__database.connection.cursor()
        cursor.execute(SQL_SELECT_MANY.format('tasks', 'user = {}'.format(user)))
        return cursor.fetchall()

    def delete(self, id):
        cursor = self.__database.connection.cursor()
        cursor.execute(SQL_DELETE_WHERE.format('tasks','id = ' + str(id)))
        self.__database.connection.commit()
