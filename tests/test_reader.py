import simplemonads as sm

try:

    class Deps(sm.Protocol):
        "Dependencies for your application"

        def popup(self, msg: str) -> None:
            "Display a popup with the specified message."


except:
    pass


def make(create: "sm.Callable[[],sm.Any]") -> "sm.Callable[[],Deps]":
    gui = create()

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


def matches(x, expected):
    assert x is expected


def err(x):
    raise Exception(x)


def test_app_is_reader():
    matches(type(app()), sm.Reader)


def test_app_contains_42():
    assert 42 == (app() + make(sm.Printer)) | {sm._: lambda x: x | {sm._: lambda x: x}}


def test_app_calls_deps():
    class TestPrinter:
        def __getattr__(self, name):
            return lambda x: equals(x, "Answer to the Universe: 42")

    app() + make(TestPrinter)


def test_just_with_none_returns_nothing():
    sm.Just(None) + (lambda x: matches(x, sm.Nothing))


def test_just_matched_with_none_matches_nothing():
    sm.Just(None) | {
        sm.Just: lambda x: equals("should not be Just", ""),
        sm.Nothing: lambda x: matches("should be nothing", "should be nothing"),
    }


def test_success_with_error_returns_failure():
    sm.Success() + (lambda x: err("fail")) + (lambda x: matches(x, sm.Failure))


def test_app_arguments_with_div_by_zero():
    class TestPrinter:
        def __getattr__(self, name):
            msg = "Whoops, an error happened: Error: division by zero"
            return lambda x: equals(x, msg)

    app(divide_by_zero=True) + make(TestPrinter)


def test_protocol():
    def ex(sut: "sm.Monad"):
        assert sut is not None

    ex(sm.Printer())
    ex(sm.BaseMonad())
    ex(sm._())
    ex(sm.Success())
    ex(sm.Failure())
    ex(sm.Just())
    ex(sm.Nothing())
    ex(sm.Lists())
    ex(sm.Reader())
    ex(sm.Future())
