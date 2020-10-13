from simplemonads import *

class AppDeps:
    def __init__(self):
        self.gui = Printer()
        
def app():
    div_by_zero = lambda x: x + (lambda x: x / 0)
                                # uncomment below to see 'Whoops, an error happened'
    data = Success(Just(7))      #+ div_by_zero 
 
    double = lambda x: x + (lambda y: y * 2)
    triple = lambda x: x + (lambda y: y * 3)
 
    result = data + triple + double
    
    def show(deps: AppDeps):
        return result | {
            Success:lambda x: x | {
                Just:lambda val: deps.gui.Popup(f'Answer to the Universe: {val}')
            },
            Failure:lambda x: deps.gui.Popup('Whoops, an error happened', x)
        } is result or result
    
    return Reader(show)
 
def main():        
    app() + AppDeps # run with default dependencies

    class GuiDeps(AppDeps):
        def __init__(self):
            try:
                import PySimpleGUI
                gui = PySimpleGUI
                self.gui = gui                        
            except:
                self.gui = Printer()

    app() + GuiDeps # run with gui dependencies

def test_app():
    assert type(app()) is Reader

if __name__ == '__main__':
    main()
