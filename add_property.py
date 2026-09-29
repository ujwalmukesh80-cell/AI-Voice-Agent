import json
import os
from flask import Blueprint, render_template, request, redirect, current_app
from werkzeug.utils import secure_filename

add_property_bp = Blueprint("add_property", __name__)


def load_json(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except:
        return []


def save_properties(properties):
    with open("properties.json", "w") as file:
        json.dump(properties, file, indent=4)


@add_property_bp.route("/add_property", methods=["GET", "POST"])
def add_property():

    if request.method == "POST":

        properties = load_json("properties.json")

        # Upload Image
        image = request.files["image"]

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        new_property = {
            "id": len(properties) + 1,
            "type": request.form["type"],
            "city": request.form["city"],
            "area": request.form["area"],
            "bhk": request.form["bhk"],
            "price": int(request.form["price"]),
            "status": request.form["status"],
            "image": filename
        }

        properties.append(new_property)

        save_properties(properties)

        return redirect("/properties")

    return render_template("add_property.html")