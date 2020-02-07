import hashlib
import random
import uuid
from check import Check
from tests import Tests


class CreateAndChange(Check, Tests):
    '''Данный класс, непосредственно, влияет на записи БД'''

    def __init__(self):
        '''Tests - для тестирования новых переданных данных, Check - для измененного обращения к БД'''
        self.Check = Check()
        self.Tests = Tests()

    def _createStartId(self):
        '''Создание стартового идентификатора, которое будет вызываться только при регистрации'''
        while True:
            # Цикл бесконечный, чтобы сгенерировался точно новый идентификатор
            ju = str(uuid.uuid4())
            nms = int("".join([i for i in ju if i.isnumeric()])[0:10])
            # Вытаскиваем все цифры из только что сгенерированного uuid
            wr = str(nms) + str(random.randint(1, 999))
            # Прибавляем к нему немного рандомных чисел
            if self.Check._checkReach(wr, 'START_ID', False):
                # Обращаемся к БД, чтобы узнать нет ли там такого идентификатора
                break
        return wr

    def _hashPassw(self, passw):
        '''Создание хэша пароля'''
        return hashlib.md5(bytes(passw, encoding='utf-8')).hexdigest()

    def _changePassw(self, email, oldPassw, newPassw):
        '''Метод, позволяющий изменить пароль'''
        if False in [self.Check._checkUser(email, oldPassw),
                    # Существует ли в БД такой пользователь?
                    self.Tests._testPassw(newPassw)]:
                    # Тестирование нового пароля
                    # oldPassw != newPassw
            return False
        else:
            newPassw = self._hashPassw(newPassw)
            # Хэш нового пароля
            if oldPassw == newPassw:
                return False
            # Не равен ли хэш нового пароля своему предку?
            self.Check.curs.execute('''UPDATE social_terminal SET PASSW=%(newPassw)s
            WHERE EMAIL=%(email)s
            AND PASSW=%(oldPassw)s''', {'newPassw': newPassw,
                                        'email': email,
                                        'oldPassw': oldPassw})
            self.Check.conn.commit()
            # Запрос и обновление БД
            return True

    def _changeEmail(self, oldEmail, passw, newEmail):
        '''Метод, позволяющий изменить почту'''
        # Здесь нам чистый пароль уже нужен
        if False in [self.Check._checkUser(oldEmail, passw),
                    # Существует ли в БД такой пользователь?
                    self.Tests.testEmail(newEmail),
                    # Тестирование новой почты
                    oldEmail != newEmail,
                    # Не равна ли эта почта своему предку?
                    self.Check._checkReach(newEmail, 'email', False)]:
                    # А не занята ли новая почта?
            return False
        else:
            self.Check.curs.execute('''UPDATE social_terminal SET EMAIL=%(newEmail)s
            WHERE EMAIL=%(oldEmail)s
            AND PASSW=%(passw)s''', {'newEmail': newEmail,
                                    'oldEmail': oldEmail,
                                    'passw': passw})
            self.Check.conn.commit()
            # Запрос и обновление БД
            return True

    def _changeNowId(self, email, passw, start_id, now_old_id, now_new_id):
        '''Метод, позволяющий изменить собственный идентификатор'''
        if False in [self.Check._checkUser(email, passw),
                    # Существует ли в БД такой пользователь?
                    self.Check._checkReach(now_new_id, 'NOW_ID', False),
                    # А не занят ли новый идентификатор?
                    start_id != now_new_id,
                    # Не равен ли этот идентификатор стартовому?
                    now_new_id != now_old_id]:
                    # А текущему (если таковой имеется?)
            return False
        else:
            self.Check.curs.execute('''UPDATE social_terminal SET NOW_ID=%(now_id)s
            WHERE EMAIL=%(email)s
            AND PASSW=%(passw)s''', {'now_id': now_new_id,
                                    'email': email,
                                    'passw': passw})
            self.Check.conn.commit()
            # Запрос и обновление БД
            return True

    def _changeName(self, email, passw, oldName, newName):
        '''Метод, позволяющий изменить имя пользователя'''
        if False in [self.Check._checkUser(email, passw),
                    # Существует ли в БД такой пользователь?
                    self.Tests.testName(newName),
                    # Тестирование нового имени
                    oldName != newName]:
                    # Не равно ли это имя своему предку?
            return False
        else:
            self.Check.curs.execute('''UPDATE social_terminal SET NAME=%(newName)s
            WHERE EMAIL=%(email)s
            AND PASSW=%(passw)s''', {'newName': newName,
                                    'email': email,
                                    'passw': passw})
            self.Check.conn.commit()
            # Запрос и обновление БД
            return True