import mysql.connector


class Check:
    '''Основная цель данного класса заключается только в обращении к БД для проверки чего-либо'''

    def __init__(self):
        '''Создание курсора и соединения, которые будут во всех унаследованных классов'''
        self.conn = mysql.connector.connect(user='root', host='localhost', database='python', password='')
        self.curs = self.conn.cursor(buffered=True)

    def _checkColumn(self, where):
        '''Метод-пощник, проверяющий существование какого либа столбца (where) в БД'''
        self.curs.execute('DESCRIBE social_terminal')
        data = ''
        # Начинаем считывать данные из результата запроса курсора, при условии что данные по умолчанию == '', а результат в своей последней итерации станет None
        while data is not None:
            if data != '':
                if where.upper() == data[0]:
                    return True
            data = self.curs.fetchone()
        return False

    def _checkReach(self, what, where, choice):
        '''Метод, позволяющий узнать, присутствует (choice == True) или отсутствует (choice == False) в определенном столбце (where) в БД некоторая запись (what)'''
        if not self._checkColumn(where):
            # Проверяем существование столбца
            return None
        else:
            self.curs.execute('SELECT ' + where.upper() + ' FROM social_terminal')
            data = ''
            # Считывая данные, мы постоянно обращаем внимание на то, что не равны ли они искомой записи. Если это случилось, то возращаем булево значение, соответствующее переданному choice
            while data is not None:
                if data != '':
                    if what == data[0]:
                        return True if choice is True else False
                data = self.curs.fetchone()
        return False if choice is True else True

    def _checkUser(self, email, passw):
        '''Метод, производящий самую обычную проверку на существование пользователя'''
        self.curs.execute('SELECT EMAIL, PASSW FROM social_terminal')
        # Начинаем считывать данные из результата запроса курсора, при условии что данные по умолчанию == (), т.к. хотим получить два значения, а результат в своей последней итерации станет None
        data = ()
        while data is not None:
            if data != ():
                if (email, passw) == data:
                    return True
            data = self.curs.fetchone()
        return False