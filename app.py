from flask import Flask
from os import getenv
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes 

if __name__ == "__main__":
    app.run(debug=True)