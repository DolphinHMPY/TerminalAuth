from at_home import AtHome
from create_and_change import CreateAndChange


class Registration(CreateAndChange):
    '''Класс регистрации'''

    def __init__(self, email, passw, name):
        '''Инициализация, в которой, по сути, нужно всё'''
        self.CreateAndChange = CreateAndChange()
        self.Tests = self.CreateAndChange.Tests
        self.Check = self.CreateAndChange.Check
        self.email = email
        self.passw = passw
        self.name = name
        self.start_id = '0'

    def endGame(self):
        '''Неожиданный конец этой регистрации, т.к. всё есть в классах-родителях'''
        if False in [self.Tests.testEmail(self.email),
                    # Тестирование почты
                    self.Tests._testPassw(self.passw),
                    # Тестирование пароля
                    self.Tests.testName(self.name),
                    # Тестирование имени
                    self.Check._checkReach(self.email, 'email', False)]:
                    # Не занята ли почта кем-либо?
            return False
        else:
            self.start_id = self.CreateAndChange._createStartId()
            # Создание стартового идентификатора
            self.passw = self.CreateAndChange._hashPassw(self.passw)
            # Хэшируем пароль
            self.Check.curs.execute('''
            INSERT INTO social_terminal(`EMAIL`, `PASSW`, `NAME`, `START_ID`)
            VALUES
            (%(email)s, %(passw)s, %(name)s, %(start_id)s)''', {'email': self.email,
                                                                'passw': self.passw, 
                                                                'name': self.name,
                                                                'start_id': self.start_id})
            self.Check.conn.commit()
            # Запрос и обновление БД
            return AtHome(self.email, self.passw, self.name, self.start_id)