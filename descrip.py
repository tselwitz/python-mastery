# descrip.py

class Descriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        print('%s:__get__' % self.name)

    def __set__(self, instance, value):
        print('%s:__set__ %s' % (self.name, value))

    def __delete__(self, instance):
        print('%s:__delete__' % self.name)


if __name__ == "__main__":
    class Foo:
        a = Descriptor('a')
        b = Descriptor('b')
        c = Descriptor('c')
    f = Foo()
    f
    f.a
    f.b
    f.a = 23
    del f.a
