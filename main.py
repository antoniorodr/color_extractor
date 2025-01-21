from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import numpy as np


app = Flask(__name__)

bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/colors")
# def get_colors():
#     np.unique(img.reshape(-1, img.shape[2]), axis=0)



if __name__ == "__main__":
    app.run(debug = True)