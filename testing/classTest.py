#classTest
class A(object):
    def __init__(self):
        x = 'Hello'

    def method_a(self, foo):
        print(x + ' ' + foo)
        
a = A()
a.method_a('sailor')
