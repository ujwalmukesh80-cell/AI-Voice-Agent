from db import get_connection


def _business_id():
    try:
        from flask import session
        return session.get("business_id")
    except Exception:
        return None


def get_all_leads(business_id=None):
    business_id = business_id or _business_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM leads WHERE business_id=?",
        (business_id,)
    )

    leads = cursor.fetchall()
    conn.close()

    return leads


def add_lead(lead, business_id=None):
    business_id = business_id or _business_id()

    if not business_id:
        raise ValueError("No business is logged in")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leads
        (name, phone, email, interested_property, status, business_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        lead["name"],
        lead["phone"],
        lead["email"],
        lead["interested_property"],
        lead["status"],
        business_id
    ))

    conn.commit()
    conn.close()


def get_lead(lead_id, business_id=None):
    business_id = business_id or _business_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM leads WHERE id=? AND business_id=?",
        (lead_id, business_id)
    )

    lead = cursor.fetchone()
    conn.close()

    return lead


def update_lead(lead_id, lead, business_id=None):
    business_id = business_id or _business_id()

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
        WHERE id=? AND business_id=?
    """, (
        lead["name"],
        lead["phone"],
        lead["email"],
        lead["interested_property"],
        lead["status"],
        lead_id,
        business_id
    ))

    conn.commit()
    conn.close()


def delete_lead(lead_id, business_id=None):
    business_id = business_id or _business_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM leads WHERE id=? AND business_id=?",
        (lead_id, business_id)
    )

    conn.commit()
    conn.close()