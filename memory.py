last_properties = []


def save_properties(properties):
    global last_properties
    last_properties = properties


def get_last_property():
    if last_properties:
        return last_properties[0]
    return None
def get_last_property():

    if not last_properties:
        return None

    return last_properties[0]