from flask import Blueprint, jsonify
from db import get_connection

api = Blueprint("api", __name__)

@api.route("/api/leads")
def api_leads():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")

    rows = cursor.fetchall()

    conn.close()

    leads = []

    for row in rows:
        leads.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "property": row[3]
        })

    return jsonify(leads)