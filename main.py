from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap5
import numpy as np
from PIL import Image
from collections import Counter
import os

app = Flask(__name__)

bootstrap = Bootstrap5(app)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        pass
    return render_template("index.html")


@app.route("/colors", methods = ["POST"])
def get_colors():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        e = "No file was uploaded"
        return render_template("error.html", error = e)
    try:
        image = Image.open(uploaded_file).convert("RGB")
        image = image.resize((100, 100))
        pixels = np.array(image).reshape(-1, 3)
        counter = Counter(map(tuple, pixels))
        total_pixels = sum(counter.values())
        top_colors = counter.most_common(10)
        color_data = [
            {
                "hex": "#{:02x}{:02x}{:02x}".format(*color),
                "percentage": round((count / total_pixels) * 100, 2)
            }
            for color, count in top_colors
        ]

        image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        image.save(image_path)

        return render_template(
            "result.html",
            color_data=color_data,
            image_url=url_for("static", filename=f"uploads/{uploaded_file.filename}")
        )
    except Exception as e:
        return render_template("error.html", error = e)

if __name__ == "__main__":
    app.run(debug = True)