from inlet import Inlet
from registration import Registration


class Wish():

    def __init__(self, email='barca@fgh.sdjy', passw='12344tyh346j', name='rusu'):
        print('What do you want?')
        print('[1]: REGISTRATION')
        print('[2]: INLET')
        print('[?]: EXIT')
        try:
            self.choice = int(input('YOUR CHOICE: '))
        except ValueError:
            self.choice = 0
        self.email = email
        self.passw = passw
        self.name = name

    def check(self):
        if self.choice not in [1, 2]:
            exit('OK, TILL...')
            return False
        else:
            if self.choice == 1:
                return Registration(self.email, self.passw, self.name)
            else:
                return Inlet(self.email, self.passw)

print(Wish().check().endGame()._getAll())