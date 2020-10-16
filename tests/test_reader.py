from simplemonads import Success, Failure, Just, _, Reader, run, Printer

class AppDeps:
    def __init__(self, gui=Printer()):
        self.gui = gui
 
def app(divide_by_zero=False):                      
    data = Success(Just(7))     
    double = lambda x: x + (lambda y: y * 2)
    triple = lambda x: x + (lambda y: y * 3)
    result = data + triple + double  

    if divide_by_zero:
        result += (lambda x: x + (lambda x: x / 0))
    
    def effect(deps: AppDeps):
        return result | {
            Success:lambda x: x | {
                Just:lambda val: deps.gui.Popup('Answer to the Universe: ' + str(val))
            },
            Failure:lambda x: deps.gui.Popup('Whoops, an error happened: ' + x)
        } is result or result
    
    return Reader(effect)
 
class GuiAppDeps(AppDeps):
    def __init__(self, gui=Printer()):
        try:
            import PySimpleGUI
            self.gui = PySimpleGUI                        
        except:
            self.gui = gui
      
@run 
def main():        
    return app() + GuiAppDeps 

def test_app_is_reader():
    assert type(app()) is Reader

def test_app_contains_42():
    assert 42 == app() + AppDeps | { _: lambda x: x | { _: lambda x: x }} 

def test_app_calls_deps():
    class TestPrinter:
        def __getattr__(self, name):
            return lambda x: self.equals(x, "Answer to the Universe: 42")
 
        def equals(self, x, expected):
            assert x == expected
   
    app() + (lambda: AppDeps(TestPrinter()))

def test_app_arguments_with_div_by_zero():
    class TestPrinter:
        def __getattr__(self, name):
            msg = "Whoops, an error happened: Error: division by zero"
            return lambda x: self.equals(x, msg)
 
        def equals(self, x, expected):
            assert x == expected
 
    app(divide_by_zero=True) + (lambda: AppDeps(TestPrinter())) 
