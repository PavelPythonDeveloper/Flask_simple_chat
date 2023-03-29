from app import app, db
from app.models import User


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
