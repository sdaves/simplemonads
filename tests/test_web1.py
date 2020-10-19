from test_reader import app, run, Printer


def produce_dict(*_):
    item = dict()
    item["count"] = 0
    return item


class Web:
    def popup(self, x):
        try:
            browser = __import__("browser")
        except:
            browser = Printer()

        tpl = '<button v-on:click="count++">' + x + " - {{ count }} times.</button>"
        browser.window.Vue.component(
            "button-counter",
            {"data": produce_dict, "template": tpl},
        )
        browser.window.Vue.new({"el": ".web1"})


@run
def main():
    return app() + Web
