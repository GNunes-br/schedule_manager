import MySQLdb
conn = MySQLdb.connect(user='root', passwd='admin', host='127.0.0.1', port=3306, charset='utf8')

create_tables = '''SET NAMES utf8;
    CREATE DATABASE `schedule`  DEFAULT CHARSET=utf8;
    USE `schedule`;
    CREATE TABLE `users` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(20) NOT NULL,
      `email` varchar(20) NOT NULL,
      `password` varchar(8) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB;
      CREATE TABLE `tasks` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `user` int NOT NULL,
      FOREIGN KEY (user) REFERENCES users(id),
      `name` varchar(50) NOT NULL,
      `description` varchar(255) NOT NULL,
      `situation` varchar(50) NOT NULL,
      `created_at` TIMESTAMP DEFAULT NOW() NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB;
    '''

drop_database = '''
    DROP DATABASE schedule
    '''

conn.cursor().execute(create_tables)