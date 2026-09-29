import re

def extract_filters(query):

    q = query.lower()

    city = None
    area = None
    property_type = None
    bhk = None
    max_price = None

    # ---------- Cities ----------

    if "hyderabad" in q:
        city = "Hyderabad"

    elif "bangalore" in q:
        city = "Bangalore"

    # ---------- Areas ----------

    areas = [
        "kondapur",
        "gachibowli",
        "madhapur",
        "shamshabad",
        "whitefield"
    ]

    for a in areas:
        if a in q:
            area = a.title()

    # ---------- Property ----------

    if "apartment" in q:
        property_type = "Apartment"

    elif "villa" in q:
        property_type = "Villa"

    elif "plot" in q:
        property_type = "Plot"

    # ---------- BHK ----------

    match = re.search(r'([1-5])\s*bhk', q)

    if match:
        bhk = match.group(1) + "BHK"

    # ---------- Budget ----------

    lakh = re.search(r'(\d+)\s*lakh', q)

    if lakh:
        max_price = int(lakh.group(1)) * 100000

    crore = re.search(r'(\d+)\s*crore', q)

    if crore:
        max_price = int(crore.group(1)) * 10000000

    return city, area, property_type, bhk, max_price