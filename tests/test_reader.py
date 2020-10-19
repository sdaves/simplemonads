from simplemonads import Failure, Just, Printer, Reader, Success, _, run

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

        def __setattr__(self, name, value):
            "Block attempts to change this class"

    return GuiDeps


def app(divide_by_zero: bool = False) -> Reader:
    data = Success(Just(7))
    double = lambda x: x + (lambda y: y * 2)
    triple = lambda x: x + (lambda y: y * 3)
    result = data + triple + double

    if divide_by_zero:
        result += lambda x: x + (lambda x: x / 0)

    def effect(deps: "Deps") -> "Union[Success, Failure]":
        msg = "Answer to the Universe: "
        err = "Whoops, an error happened: "
        result | {
            Success: lambda x: x | {Just: lambda val: deps.popup(msg + str(val))},
            Failure: lambda x: deps.popup(err + x),
        }
        return result

    return Reader(effect)


@run
def main():
    return app() + make(
        Success() + (lambda: __import__("PySimpleGUI"))
        | {Success: lambda x: x, Failure: lambda x: Printer}
    )


def equals(x, expected):
    assert x == expected


def test_app_is_reader():
    assert type(app()) is Reader


def test_app_contains_42():
    assert 42 == app() + make(Printer) | {_: lambda x: x | {_: lambda x: x}}


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
