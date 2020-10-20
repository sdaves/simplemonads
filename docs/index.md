# simplemonads

Let's make monads easy, fun, and productive.

## Just, Nothing, Pattern matching

Using Just means you get to pattern match against the monad and remove all None (Nothing monad) instances. This removes the need to check values for None, or should I say it removes the forgetting of checking the values for None?

Being able to pipe a monad into a dictionary makes it easy to filter values, and without the need for more keywords in the language! If you don't like the pipe syntax `|` you can use the match method instead. The library includes the  `_` monad that allows matching unknown monads in the dictionary. Yes I do hope Guido merges his pattern matching into Python 3 mainline, but I'm not holding my breath ...

```python
import simplemonads as sm
assert 1 == sm.Just(1).match({ sm._: lambda x: x })
assert 'nada' == sm.Nothing() | { sm.Just: lambda x: 'found', sm._: lambda x: 'nada' }
```

## Success, Failure 

Tired of forgetting about unhandled exceptions? Stop worring about it and use the Success monad!

```python
import simplemonads as sm        #this would normally throw a ZeroDivisionError exception and blow up the program
assert 'nope' == sm.Success(42) + (lambda x: x / 0) | { sm.Success: lambda x: 'works', sm.Failure: lambda x: 'nope' }
assert 84 == sm.Success(42) + (lambda x: x * 2) | { sm.Success: lambda x: x, sm.Failure: lambda x: 0 }
```

## Future 

Async has many useful cases in python and making it easy is important. The issue in python is that once you make you function async, all other functions have to be async to use yours. This becomes like a virus where you have to make EVERYTHING async, which is silly if you are not doing async work in all your function. Say goodbye to async spread and easily use your async function from within any normal function.

```python
import simplemonads as sm

async def doubler(x:int):
    import asyncio
    await asyncio.sleep(1)
    return x * 2
    
assert 84 == sm.Future(42) + doubler | { sm.Future: lambda x: x }
```

Async functions can also be chained together for multiple effects in a pipeline.

```python
from simplemonads import Future

async def effect(data=1):
    import asyncio
    await asyncio.sleep(0.1)
    return data ** data

assert Future(2) | { Future: lambda x: x } == 2

assert Future(2) + effect | { Future: lambda x: x } == 4

assert Future(2) + effect + effect | { Future: lambda x: x } == 256

```

## Reader

It can be frusterating just how many imports you need to do to get a program working, but do I really need all that imported to do meaningful work? What about when I need to test my code, how to I make it stop using all those imports? Using the Reader monad allows having dependencies injected at runtime, enabling dependency free code that is easier to test and make work across platforms.

```python
import simplemonads as sm
from typing import Protocol

class Deps(Protocol):
    def send_email(self, from_email, to_email, subject, body):
        "Send an email"

def make(make_mailer):
    mailer = make_mailer()
    class AppDeps:
        def send_email(self, from_email, to_email, subject, body):
            mailer.send(from_email, to_email, subject, body)
    return AppDeps

def app():
    def effect(deps: Deps):
        deps.send_email('me@mydomain.com', 'friend@somewhere.com', 'Hey, check out my cool cat photos', 'blah blah blah, and many links to cats')
        
    return sm.Reader(effect)

@sm.run
def main(make_mailer=lambda: sm.Printer()):
    return app() + make(make_mailer)
```

This allows injecting new make_reader functions into the main function, rather than the dummy Printer that just prints stuff to the console, and these can be specified by another file that does all the import wizardry. With these techniques it is possible to follow clean architecture guidelines and not have implementation details in your business logic code.
