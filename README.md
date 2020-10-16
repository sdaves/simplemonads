# simplemonads

Simple Monads for Python. Use Just to end checking for None, Success to end unhandled exceptions, and Reader for dependency injection.

![Screenshot of test_reader.py](https://imgur.com/ZnAwyVc.png)


## Example using monads: `Success`, `Failure`, `Just`, `Reader`, and `Printer`

```python
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
```

## Handling exceptions

To demonstrate exception handling the above example can be changed to:

```python
    return app(True) + GuiAppDeps
```

This will result in safely handling the divide by zero exception and will run the following without interrupting the flow of the application:

```python
            Failure:lambda x: deps.gui.Popup('Whoops, an error happened: ' + x)
```
