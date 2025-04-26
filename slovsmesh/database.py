import sqlite3


class Database:
    __conn = None

    def __init__(self, db_path):
        self.__conn = sqlite3.connect(db_path, check_same_thread=False)

        self.__ping()
        self.__create_table()

    def __create_table(self):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()

                cursor.execute('create table if not exists scores (name varchar(20), score integer)')
                cursor.execute('create index if not exists scores_name_index on scores (name)')

                self.__conn.commit()
        except Exception as e:
            raise ConnectionError('Не могу создать таблицу scores') from e
    
    def __ping(self):
        try:
            with self.__conn:
                cursor = self.__conn.cursor()
                cursor.execute('select 1')

                results = cursor.fetchone()
                if results is None or results[0] != 1:
                    raise ConnectionError('База данных недоступна')
        except Exception as e:
            raise ConnectionError('Не могу подключиться к базе данных') from e
    
    def get_scores(self):
        with self.__conn:
            cursor = self.__conn.cursor()
            cursor.execute('select name, score from scores order by score desc limit 10')
            
            return [{'user_name': score[0], 'score': score[1]} for score in cursor.fetchall()]
    
    def put_score(self, user_name, score):
        with self.__conn:
            cursor = self.__conn.cursor()
            cursor.execute('insert into scores (name, score) values (?, ?)', (user_name, score))
            
            self.__conn.commit()
