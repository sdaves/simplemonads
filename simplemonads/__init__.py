'''Easy to use monads (containers) that improve the quality of your python code.'''

class Monad:
    '''The base monad and implementation of the bind notation along with shortcuts (+) for binding, and (|) for matching.'''
    def __init__(self, value=None):
        self._value = value
        
    def bind(self, fn):
        '''Bind lifts the value from self._value into the function argument according to the laws of this monad.'''
        return self
 
    def match(self, items={}):
        '''Pattern match the `items` dictionary with `self._value` and return a monad.'''
        keys = list(items.keys())
        locate = type(self)
        if not items:
            print('DEBUG: ' + str(self._value))
        if locate in keys:
            return items[locate](self._value)
        if _ in keys:
            return items[_](self._value)
        return self
 
    def __or__(self, items={}):
        '''Calls `match` class method.'''
        return self.match(items)
        
    def __add__(self, fn):
        '''Calls `bind` class method.'''
        return self.bind(fn)
        
    def __str__(self):
        return str(type(self)) + ' ' + str(self._value)
 
class _(Monad):
    pass
 
class Failure(Monad):
    pass
 
class Success(Monad):
    '''Lift the value in self._value into the function argument and return a Success monad.'''
    def bind(self, fn):
        try:
            return Success(fn(self._value))
        except Exception as ex:
            return Failure('Error: ' + str(ex))
 
class List(Monad):
    def bind(self, fn):
        return List(list(map(fn, self._value)))
 
class Nothing(Monad):
    def bind(self, fn):
        return Nothing()
    
class Just(Monad):
    def bind(self, fn):
        return Just(fn(self._value))    
 
class Reader(Monad):
    '''Inject dependencies into the self._value function when binding to the monad.'''
    def bind(self, fn):
        return self._value(fn())
        
class Printer(Monad):
    def __getattr__(self, name):
        return print
    
