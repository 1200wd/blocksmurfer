from blocksmurfer import current_app
from config import Config

app = current_app(Config)

if __name__ == "__main__":
    app.run()
