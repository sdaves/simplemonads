import simplemonads as sm
from test_reader import TestReader


def produce_dict(*_):
    item = dict()
    item["count"] = 0
    return item


class Web:
    def popup(self, x):
        try:
            browser = __import__("browser")
        except:
            browser = sm.Printer()

        tpl = '<button v-on:click="count++">' + x + " - {{ count }} times.</button>"
        browser.window.Vue.component(
            "button-counter",
            {"data": produce_dict, "template": tpl},
        )
        browser.window.Vue.new({"el": ".web1"})


@sm.run
def main():
    return TestReader.app() + Web
