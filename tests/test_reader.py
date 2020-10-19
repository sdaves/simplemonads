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


def equals(x, expected):
    assert x == expected


def test_app_is_reader():
    assert type(app()) is sm.Reader


def test_app_contains_42():
    assert 42 == (app() + make(sm.Printer)) | {sm._: lambda x: x | {sm._: lambda x: x}}


def test_app_calls_deps():
    class TestPrinter:
        def __getattr__(self, name):
            return lambda x: equals(x, "Answer to the Universe: 42")

    app() + make(TestPrinter)


def test_app_arguments_with_div_by_zero():
    class TestPrinter:
        def __getattr__(self, name):
            msg = "Whoops, an error happened: Error: division by zero"
            return lambda x: equals(x, msg)

    app(divide_by_zero=True) + make(TestPrinter)
