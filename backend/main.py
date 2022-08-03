from application import create_app
from deta import App

app = App(create_app())

if __name__ == "__main__":
    app.run()
