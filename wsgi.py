from src.app import App

app = App().flask_app

if __name__ == "__main__":
    app.run(threaded=True)
