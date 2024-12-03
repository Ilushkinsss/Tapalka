import psycopg2
from psycopg2 import sql
import config

class Database:
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def create_users_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            total_points INTEGER DEFAULT 0,
            total_referrals INTEGER DEFAULT 0,
            total_tasks INTEGER DEFAULT 0,
            company VARCHAR(255),
            lvl_points INTEGER DEFAULT 0
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def create_referrals_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS referrals (
            id SERIAL PRIMARY KEY,
            user_request_telegram_id BIGINT NOT NULL,
            user_invited_telegram_id BIGINT NOT NULL
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def create_tasks_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL,
            task_points INTEGER NOT NULL,
            task_description TEXT,
            task_url VARCHAR(255)
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def create_completed_tasks_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS completed_tasks (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            task_id INTEGER REFERENCES tasks(id)
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()
