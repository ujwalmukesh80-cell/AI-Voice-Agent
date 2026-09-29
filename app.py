from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash
)
from recommender import recommend
from chatbot import get_response
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather
from ai.brain import ask_ai
from property_search import search_property, format_property
from lead_capture import save_lead
from sms import send_confirmation
from booking_manager import save_booking
from call_logger import save_call

from werkzeug.utils import secure_filename

import os
import json
import property_db
import lead_db
import traceback

customer = {
    "stage": "search",
    "name": "",
    "phone": "",
    "property": "",
    "requirement": "",
    "date": "",
    "time": ""
}



app = Flask(__name__)
app.secret_key = "realestate_secret_key"

from api import api
app.register_blueprint(api)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# JSON Helper Functions
# -----------------------------

def load_json(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except:
        return []


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------
# Login
# -----------------------------
@app.route("/dashboard-ai")
def dashboard_ai():

    if not session.get("logged_in"):
        return redirect("/login")

    return render_template("dashboard_ai.html")
@app.route("/call_logs")
def call_logs():

    with open("call_logs.json", "r") as f:
        logs = json.load(f)

    return render_template(
        "call_logs.html",
        logs=logs
    )
@app.route("/voice", methods=["POST"])
def voice():

    global customer

    speech = request.values.get("SpeechResult")

    response = VoiceResponse()

    # First Call
    if not speech:

        gather = Gather(
            input="speech",
            action="/voice",
            method="POST",
            speechTimeout="auto",
            timeout=8,
            language="en-IN"
        )

        gather.say(
            "Hello. Welcome to AI Real Estate Assistant. Please tell me what property you are looking for.",
            voice="alice"
        )

        response.append(gather)

        return str(response)

    print("Customer:", speech)

    try:

        # ---------------- SEARCH ----------------

        if customer["stage"] == "search":

            property_data = search_property(speech)

            if property_data:

                customer["property"] = (
                    property_data["type"] + " - " + property_data["area"]
                )

                customer["requirement"] = speech

                customer["stage"] = "booking"

                reply = format_property(property_data)

            else:

                reply = ask_ai(speech)

        # ---------------- BOOKING ----------------

        elif customer["stage"] == "booking":

            if speech.lower() in ["yes", "schedule", "book", "site visit"]:

                customer["stage"] = "name"

                reply = "Great. May I know your name?"

            else:

                reply = "Would you like to schedule a site visit?"

        # ---------------- NAME ----------------

        elif customer["stage"] == "name":

            customer["name"] = speech

            customer["stage"] = "phone"

            reply = "May I have your mobile number?"

        # ---------------- PHONE ----------------

        elif customer["stage"] == "phone":

            phone = speech.replace(" ", "").replace("-", "")

            if len(phone) < 10 or not phone.isdigit():

                reply = "That doesn't seem to be a valid phone number. Please repeat your mobile number."

            else:

                customer["phone"] = phone

                save_lead(
                    customer["name"],
                    customer["phone"],
                    customer["requirement"]
                )

                customer["stage"] = "date"

                reply = "What date would you like to visit?"

        # ---------------- DATE ----------------

        elif customer["stage"] == "date":

            customer["date"] = speech

            customer["stage"] = "time"

            reply = "At what time would you like to visit?"

        # ---------------- TIME ----------------

        elif customer["stage"] == "time":

            customer["time"] = speech

            save_booking(
                customer["name"],
                customer["phone"],
                customer["property"],
                customer["date"],
                customer["time"]
            )
            save_call(
                customer["name"],
                customer["phone"],
                customer["requirement"],
                customer["property"]
            )   
            send_confirmation(
               customer["name"],
               customer["phone"],
               customer["property"],
               customer["date"],
               customer["time"]
                         )

            customer = {
                "stage": "search",
                "name": "",
                "phone": "",
                "property": "",
                "requirement": "",
                "date": "",
                "time": ""
            }

            reply = (
                "Thank you. Your site visit has been booked successfully. "
                "Our sales executive will contact you shortly."
            )

        else:

            reply = ask_ai(speech)

        print("AI:", reply)

    except Exception:

        print("========== ERROR ==========")
        traceback.print_exc()
        print("===========================")

        reply = "Sorry, an internal error occurred."

    gather = Gather(
        input="speech",
        action="/voice",
        method="POST",
        speechTimeout="auto",
        timeout=8,
        language="en-IN"
    )

    gather.say(reply, voice="alice")

    response.append(gather)

    return str(response)
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login") 
# -----------------------------
# Dashboard
# -----------------------------

@app.route("/")
def dashboard():


    properties = property_db.get_all_properties()

    leads = load_json("leads.json")
    bookings = load_json("bookings.json")

    available = sum(
        1
        for p in properties
        if p["status"].lower() == "available"
    )

    sold = sum(
        1
        for p in properties
        if p["status"].lower() == "sold"
    )

    total_value = sum(
        p["price"]
        for p in properties
    )

    average_price = (
        total_value / len(properties)
        if properties else 0
    )

    return render_template(
        "index.html",
        total_properties=len(properties),
        available=available,
        sold=sold,
        total_leads=len(leads),
        total_bookings=len(bookings),
        total_value=total_value,
        average_price=average_price
    )


# -----------------------------
# Properties
# -----------------------------

@app.route("/properties")
def properties():

    if not session.get("logged_in"):
        return redirect("/login")

    properties = property_db.get_all_properties()

    return render_template(
        "properties.html",
        properties=properties
    )
# -----------------------------
# Add Property
# -----------------------------
@app.route("/add_property", methods=["GET", "POST"])
def add_property_route():

    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":

        filename = ""

        image = request.files.get("image")

        if image and image.filename != "":
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        new_property = {

            "type": request.form["type"],
            "city": request.form["city"],
            "area": request.form["area"],
            "bhk": request.form["bhk"],
            "price": int(request.form["price"]),
            "status": request.form["status"],
            "image": filename

        }

        property_db.add_property(new_property)

        flash("Property Added Successfully!")

        return redirect("/properties")

    return render_template("add_property.html")


# -----------------------------
# Edit Property
# -----------------------------
@app.route("/edit_property/<int:property_id>", methods=["GET", "POST"])
def edit_property(property_id):

    if not session.get("logged_in"):
        return redirect("/login")

    property_data = property_db.get_property(property_id)

    if property_data is None:
        return "Property Not Found"

    if request.method == "POST":

        filename = property_data["image"]

        image = request.files.get("image")

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        updated_property = {

            "type": request.form["type"],
            "city": request.form["city"],
            "area": request.form["area"],
            "bhk": request.form["bhk"],
            "price": int(request.form["price"]),
            "status": request.form["status"],
            "image": filename

        }

        property_db.update_property(
            property_id,
            updated_property
        )

        flash("Property Updated Successfully!")

        return redirect("/properties")

    return render_template(
        "edit_property.html",
        property=property_data
    )


# -----------------------------
# Delete Property
# -----------------------------
@app.route("/delete_property/<int:property_id>")
def delete_property_route(property_id):

    if not session.get("logged_in"):
        return redirect("/login")

    property_db.delete_property(property_id)

    flash("Property Deleted Successfully!")

    return redirect("/properties")
# -----------------------------
# Property Details
# -----------------------------
@app.route("/property/<int:property_id>")
def property_details(property_id):

    if not session.get("logged_in"):
        return redirect("/login")

    property_data = property_db.get_property(property_id)

    if property_data is None:
        return "Property Not Found"

    return render_template(
        "property_details.html",
        property=property_data
    )


# -----------------------------
# Leads
# -----------------------------
@app.route("/leads")
def leads():

    if not session.get("logged_in"):
        return redirect("/login")

    leads = lead_db.get_all_leads()

    return render_template(
        "leads.html",
        leads=leads
    )
@app.route("/add_lead", methods=["GET", "POST"])
def add_lead():

    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":

        lead = {

            "name": request.form["name"],
            "phone": request.form["phone"],
            "email": request.form["email"],
            "interested_property": request.form["interested_property"],
            "status": request.form["status"]

        }

        lead_db.add_lead(lead)

        flash("Lead Added Successfully!")

        return redirect("/leads")

    return render_template("add_lead.html")
@app.route("/edit_lead/<int:lead_id>", methods=["GET", "POST"])
def edit_lead(lead_id):

    if not session.get("logged_in"):
        return redirect("/login")

    lead = lead_db.get_lead(lead_id)

    if request.method == "POST":

        updated = {
            "name": request.form["name"],
            "phone": request.form["phone"],
            "email": request.form["email"],
            "interested_property": request.form["interested_property"],
            "status": request.form["status"]
        }

        lead_db.update_lead(lead_id, updated)

        flash("Lead Updated Successfully!")

        return redirect("/leads")

    return render_template(
        "edit_lead.html",
        lead=lead
    )
@app.route("/delete_lead/<int:lead_id>")
def delete_lead(lead_id):

    if not session.get("logged_in"):
        return redirect("/login")

    lead_db.delete_lead(lead_id)

    flash("Lead Deleted Successfully!")

    return redirect("/leads")
# -----------------------------
# Bookings
# -----------------------------
@app.route("/bookings")
def bookings():

    if not session.get("logged_in"):
        return redirect("/login")

    bookings = load_json("bookings.json")

    return render_template(
        "bookings.html",
        bookings=bookings
    )


# -----------------------------
# Search Properties
# -----------------------------
@app.route("/search")
def search():

    if not session.get("logged_in"):
        return redirect("/login")

    city = request.args.get("city", "").lower()
    property_type = request.args.get("type", "").lower()
    status = request.args.get("status", "").lower()
    bhk = request.args.get("bhk", "")
    max_price = request.args.get("price", "")

    properties = property_db.get_all_properties()

    filtered = []

    for p in properties:

        if city and city not in p["city"].lower():
            continue

        if property_type and property_type not in p["type"].lower():
            continue

        if status and status != p["status"].lower():
            continue

        if bhk and bhk != p["bhk"]:
            continue

        if max_price:
            try:
                if int(p["price"]) > int(max_price):
                    continue
            except:
                pass

        filtered.append(p)

    return render_template(
        "properties.html",
        properties=filtered
    )
# -----------------------------
# Error Pages
# -----------------------------
@app.errorhandler(404)
def page_not_found(error):
    return "404 Page Not Found", 404


@app.errorhandler(500)
def internal_error(error):
    return "500 Internal Server Error", 500


# -----------------------------
# Run Application
# -----------------------------

@app.route("/recommend", methods=["GET", "POST"])
def recommend_property():

    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":

        city = request.form["city"]
        area = request.form["area"]
        property_type = request.form["type"]
        bhk = request.form["bhk"]

        max_price = request.form["price"]

        if max_price:
            max_price = int(max_price)
        else:
            max_price = None

        properties = property_db.get_all_properties()

        best_property = recommend(
            properties,
            city,
            area,
            property_type,
            bhk,
            max_price
        )

        return render_template(
            "recommend.html",
            property=best_property
        )

    return render_template("recommend_form.html")
@app.route("/chat", methods=["GET", "POST"])
def chat():

    if not session.get("logged_in"):
        return redirect("/login")

    answer = ""

    if request.method == "POST":

        question = request.form["message"]

        answer = get_response(question)

    return render_template(
        "chat.html",
        answer=answer
    )
# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
