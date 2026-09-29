from lead_manager import save_lead
from memory import get_last_properties

def handle_lead(user):

    q = user.lower()

    keywords = [
        "interested",
        "book",
        "site visit",
        "visit property",
        "call me"
    ]

    if not any(word in q for word in keywords):
        return None

    props = get_last_properties()

    if not props:
        return "Please ask about a property first."

    property_name = f"{props[0]['type']} in {props[0]['area']}"

    print("\nCustomer is interested!")

    name = input("Customer Name: ")

    phone = input("Phone Number: ")

    save_lead(name, phone, property_name)

    return (
        f"Thank you {name}. "
        "Your site visit request has been saved. "
        "Our sales team will contact you soon."
    )