from property_search import search_properties

results = search_properties(
    city="Hyderabad",
    property_type="Apartment",
    max_price=5000000
)

if results:

    print("\nProperties Found:\n")

    for house in results:

        print("----------------------------")
        print("Type :", house["type"])
        print("City :", house["city"])
        print("Area :", house["area"])
        print("BHK  :", house["bhk"])
        print("Price: ₹", format(house["price"], ","))
        print("Status:", house["status"])

else:

    print("No properties found.")