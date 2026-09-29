from db import get_connection


def get_all_leads():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads")

    leads = cursor.fetchall()

    conn.close()

    return leads


def add_lead(lead):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leads
        (name, phone, email, interested_property, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        lead["name"],
        lead["phone"],
        lead["email"],
        lead["interested_property"],
        lead["status"]
    ))

    conn.commit()
    conn.close()


def get_lead(lead_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM leads WHERE id=?",
        (lead_id,)
    )

    lead = cursor.fetchone()

    conn.close()

    return lead


def update_lead(lead_id, lead):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leads
        SET
            name=?,
            phone=?,
            email=?,
            interested_property=?,
            status=?
        WHERE id=?
    """, (
        lead["name"],
        lead["phone"],
        lead["email"],
        lead["interested_property"],
        lead["status"],
        lead_id
    ))

    conn.commit()
    conn.close()


def delete_lead(lead_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM leads WHERE id=?",
        (lead_id,)
    )

    conn.commit()
    conn.close()