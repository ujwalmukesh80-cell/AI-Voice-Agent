from db import get_connection


def _business_id():
    try:
        from flask import session
        return session.get("business_id")
    except Exception:
        return None


def get_all_properties(business_id=None):
    business_id = business_id or _business_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE business_id=?",
        (business_id,)
    )

    properties = cursor.fetchall()
    conn.close()

    return properties


def add_property(property_data, business_id=None):
    business_id = business_id or _business_id()

    if not business_id:
        raise ValueError("No business is logged in")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO properties
        (type, city, area, bhk, price, status, image, business_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        property_data["type"],
        property_data["city"],
        property_data["area"],
        property_data["bhk"],
        property_data["price"],
        property_data["status"],
        property_data["image"],
        business_id
    ))

    conn.commit()
    conn.close()


def delete_property(property_id, business_id=None):
    business_id = business_id or _business_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM properties WHERE id=? AND business_id=?",
        (property_id, business_id)
    )

    conn.commit()
    conn.close()


def get_property(property_id, business_id=None):
    business_id = business_id or _business_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE id=? AND business_id=?",
        (property_id, business_id)
    )

    property_data = cursor.fetchone()
    conn.close()

    return property_data


def update_property(property_id, property_data, business_id=None):
    business_id = business_id or _business_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE properties
        SET
            type=?,
            city=?,
            area=?,
            bhk=?,
            price=?,
            status=?,
            image=?
        WHERE id=? AND business_id=?
    """, (
        property_data["type"],
        property_data["city"],
        property_data["area"],
        property_data["bhk"],
        property_data["price"],
        property_data["status"],
        property_data["image"],
        property_id,
        business_id
    ))

    conn.commit()
    conn.close()
def get_property_public(property_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE id=?",
        (property_id,)
    )

    property_data = cursor.fetchone()

    conn.close()

    return property_data