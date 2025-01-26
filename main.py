from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import numpy as np
from PIL import Image
from collections import Counter
import io
import base64

app = Flask(__name__)

bootstrap = Bootstrap5(app)

def round_color(color, factor=10):
    return tuple((value // factor) * factor for value in color)


@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("index.html")


@app.route("/colors", methods=["POST"])
def get_colors():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        e = "No file was uploaded"
        return render_template("error.html", error=e)
    try:
        image = Image.open(uploaded_file).convert("RGB")
        pixels = np.array(image).reshape(-1, 3)
        rounded_pixels = [round_color(pixel, factor=50) for pixel in pixels]
        counter = Counter(rounded_pixels)
        total_pixels = sum(counter.values())
        top_colors = counter.most_common(10)
        color_data = [
            {
                "hex": "#{:02x}{:02x}{:02x}".format(*color),
                "percentage": round((count / total_pixels) * 100, 2)
            }
            for color, count in top_colors
        ]
        img_io = io.BytesIO()
        image.save(img_io, format="PNG")
        img_io.seek(0)
        base64_img = base64.b64encode(img_io.getvalue()).decode("utf-8")
        image_url = f"data:image/png;base64,{base64_img}"
        return render_template("result.html", color_data=color_data, image_url=image_url)
    except Exception as e:
        return render_template("error.html", error=e)


if __name__ == "__main__":
    app.run(debug = True)