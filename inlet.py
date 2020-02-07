from at_home import AtHome
from create_and_change import CreateAndChange


class Inlet(CreateAndChange):
    '''Класс входа'''

    def __init__(self, email, passw):
        '''Инициализация, в которой, что странно, тоже нужно всё'''
        self.CreateAndChange = CreateAndChange()
        self.Tests = self.CreateAndChange.Tests
        self.Check = self.CreateAndChange.Check
        self.email = email
        self.passw = passw

    def endGame(self):
        '''Неожиданный конец этой регистрации, т.к. всё есть в классах-родителях'''
        if False in [self.Tests.testEmail(self.email),
                    # Тестирование почты
                    self.Tests._testPassw(self.passw),
                    # Тестирование пароля
                    self.Check._checkReach(self.email, 'email', True)]:
                    # Есть ли вообще эта почта в БД
            return False
        else:
            self.passw = self.CreateAndChange._hashPassw(self.passw)
            # Хэшируем пароль
            if self.Check._checkUser(self.email, self.passw):
                # Верна ли эта комбинация?
                return AtHome(self.email, self.passw)