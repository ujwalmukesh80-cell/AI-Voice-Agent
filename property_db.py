from db import get_connection


def get_all_properties():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties")

    properties = cursor.fetchall()

    conn.close()

    return properties


def add_property(property_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO properties
        (type, city, area, bhk, price, status, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        property_data["type"],
        property_data["city"],
        property_data["area"],
        property_data["bhk"],
        property_data["price"],
        property_data["status"],
        property_data["image"]
    ))

    conn.commit()
    conn.close()


def delete_property(property_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM properties WHERE id=?",
        (property_id,)
    )

    conn.commit()
    conn.close()


def get_property(property_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM properties WHERE id=?",
        (property_id,)
    )

    property_data = cursor.fetchone()

    conn.close()

    return property_data


def update_property(property_id, property_data):

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
        WHERE id=?
    """, (
        property_data["type"],
        property_data["city"],
        property_data["area"],
        property_data["bhk"],
        property_data["price"],
        property_data["status"],
        property_data["image"],
        property_id
    ))

    conn.commit()
    conn.close()