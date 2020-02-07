from create_and_change import CreateAndChange


class AtHome(CreateAndChange):
    '''Данный класс полностью соответствует своему имени - "дома". Именно здесь нужно сделать наиболее удобное взаимодействие с классом reateAndChange'''

    def __init__(self, email, passw, name='', start_id='0'):
        '''Остальные классы здесь уже не нужны (Check получим из reateAndChange). Причем, здесь обыгрывается тот факт, что сюда можно попасть как из Inlet'а, так и из Registration'а'''
        self.CreateAndChange = CreateAndChange()
        self.Check = self.CreateAndChange.Check
        # Если зашли с Inlet'а, то получить всю остальную информацию, с Registration'а - только текущий идентификатор (его значение по умолчанию)
        self.email = email
        self.passw = passw
        self._all = self._getAll()
        self.name = name if name != '' else self._all[0][1]
        self.start_id = start_id if start_id != '0' else self._all[0][4]
        self.now_id = self._all[0][5]

    def _getAll(self):
        '''Метод, помогающий получить всю оставшуюся информацию'''
        self.Check.curs.execute('SELECT * FROM social_terminal WHERE EMAIL = %(email)s AND PASSW = %(passw)s', {'email': self.email, 'passw': self.passw})
        return self.Check.curs.fetchall()