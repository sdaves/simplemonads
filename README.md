# simplemonads

Easy to use monads (containers) that improve the quality of your python code. Use `Just` to end checking for None, `Success` to end unhandled exceptions, `Future` for async, and `Reader` for dependencies.

## Platform support

Just `pip install simplemonads` and you're done. You can also copy the single file `simplemonads/__init__.py` into your project and use it as you wish without dependencies. Works across all platforms, so CPython >= 3.5 (Windows, Linux, Mac, Android, iOS), [in browser with Brython](https://raw.githack.com/sdaves/simplemonads/main/tests/test_brython_standalone.html), and [even on microcontrollers with micropython](https://micropython.org)!

![Screenshot of test_reader.py](https://imgur.com/ZnAwyVc.png)


## Example using monads: `Success`, `Failure`, `Just`, `Reader`, and `Printer`

```python
import simplemonads as sm

try:
    from typing import Callable, Protocol, Union, Any

    class Deps(Protocol):
        "Dependencies for your application"

        def popup(self, msg) -> None:
            "Display a popup with the specified message."


    import PySimpleGUI


except:
    pass


def make(make_gui: "Callable[[],PySimpleGUI]") -> "Callable[[],Deps]":
    gui = make_gui()

    class GuiDeps:
        def popup(self, x: str):
            gui.Popup(x)

    return GuiDeps


def app(divide_by_zero: bool = False) -> sm.Reader:
    data = sm.Success(sm.Just(7))
    double = lambda x: x + (lambda y: y * 2)
    triple = lambda x: x + (lambda y: y * 3)
    result = data + triple + double

    if divide_by_zero:
        result += lambda x: x + (lambda x: x / 0)

    def effect(deps: "Deps") -> "sm.Monad":
        msg = "Answer to the Universe: "
        err = "Whoops, an error happened: "
        result | {
            sm.Success: lambda x: x | {sm.Just: lambda val: deps.popup(msg + str(val))},
            sm.Failure: lambda x: deps.popup(err + x),
        }
        return result

    return sm.Reader(effect)


@sm.run
def main():
    lib = sm.Success() + (lambda x: __import__("PySimpleGUI"))
    gui = lib | {sm.Success: lambda x: x, sm.Failure: lambda x: sm.Printer()}
    return app() + make(lambda: gui)
```

## Handling exceptions

To demonstrate exception handling the above example can be changed to:

```python
    return app() + make(lambda: gui)
```

This will result in safely handling the divide by zero exception and will run the following without interrupting the flow of the application:

```python
            sm.Failure: lambda x: deps.popup(err + x),
```

## Example monad `Future`

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

This allows easily adding async functions into the monadic pipeline. If you need special concurrency options, you can await multiple tasks from inside the effect function.
