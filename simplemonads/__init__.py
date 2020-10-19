"Easy to use monads (containers) that improve the quality of your python code."


try:
    from typing import Callable, Protocol, Union, Any

    class Monad(Protocol):
        "The base protocol that other Monads implement."

        def bind(self, fn: "Callable") -> "Monad":
            "Perform the monadic action on the argument."

        def __add__(self, fn: "Callable") -> "Any":
            "Shortcut for `match`"

        def match(self, items: dict) -> "Monad":
            "Pattern match the `items` dictionary with `self._value` and return a monad."

        def __or__(self, items: dict) -> "Any":
            "Shortcut for `match`"


except:
    pass


class Printer:
    def __init__(self, value=None):
        self._value = value

    def bind(self, fn: "Callable") -> "Printer":
        return Printer(fn(self._value))

    def __add__(self, fn: "Callable") -> "Printer":
        return self.bind(fn)

    def match(self, items: dict) -> "Printer":
        return Printer(self._value)

    def __or__(self, items: dict) -> "Printer":
        return Printer(self._value)

    def __getattr__(self, name: str):
        return print


class BaseMonad:
    def __init__(self, value=None):
        self._value = value

    def bind(self, fn: "Callable") -> "Monad":
        "Bind lifts the value from self._value into the function argument according to the laws of this monad."
        return self

    def match(self, items={}) -> "Monad":
        "Pattern match the `items` dictionary with `self._value` and return a monad."
        keys = list(items.keys())
        locate = type(self)
        if not items:
            print("DEBUG: " + str(self._value))
        if locate in keys:
            return items[locate](self._value)
        if _ in keys:
            return items[_](self._value)
        return self

    def __or__(self, items={}) -> "Monad":
        "Calls `match` class method."
        return self.match(items)

    def __add__(self, fn: "Callable") -> "Monad":
        "Calls `bind` class method."
        return self.bind(fn)

    def __str__(self):
        return str(type(self)) + " " + str(self._value)


class _(BaseMonad):
    pass


class Failure(BaseMonad):
    pass


class Success(BaseMonad):
    "Lift the value in self._value into the function argument and return a Success monad."

    def bind(self, fn: "Callable") -> "Union[Success, Failure]":
        try:
            return Success(fn(self._value))
        except Exception as ex:
            return Failure("Error: " + str(ex))


class List(BaseMonad):
    _value = []

    def bind(self, fn: "Callable") -> "List":
        return List(list(map(fn, self._value)))


class Nothing(BaseMonad):
    def bind(self, fn: "Callable") -> "Nothing":
        return Nothing()


class Just(BaseMonad):
    def bind(self, fn: "Callable") -> "Just":
        return Just(fn(self._value))


class Reader(BaseMonad):
    "Inject dependencies into the self._value function when binding to the monad."

    def bind(self, fn: "Callable") -> "Reader":
        return self._value(fn())


class Future(BaseMonad):
    def __init__(self, value=None, loop=None):
        if not loop:
            import asyncio

            loop = asyncio.get_event_loop()

        self._value = value
        self._loop = loop
        super().__init__(value)

    def bind(self, fn: "Callable") -> "Future":
        import asyncio

        result = self._loop.run_until_complete(asyncio.gather(fn(self._value)))
        return Future(result[0], self._loop)


def run(fn: "Callable") -> "Callable":
    "If your module is the `__main__` module this decorator will run the decorated function."

    if "__main__" in fn.__module__:
        fn()

    return fn
