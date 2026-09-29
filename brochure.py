import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor

from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch


def generate_brochure(property_data):

    filename = "Property_Brochure.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER
    title.textColor = HexColor("#0B5394")

    heading = styles["Heading2"]
    heading.textColor = HexColor("#0B5394")

    story = []

    # -------------------------
    # Company Logo
    # -------------------------

    logo = "static/logo.png"

    if os.path.exists(logo):
        img = Image(logo, width=1.3*inch, height=1.3*inch)
        img.hAlign = "CENTER"
        story.append(img)

    story.append(
        Paragraph(
            "<b>DREAM HOMES</b>",
            title
        )
    )

    story.append(
        Paragraph(
            "Premium Real Estate Solutions",
            styles["Heading3"]
        )
    )

    story.append(Spacer(1, 20))

    # -------------------------
    # Property Image
    # -------------------------

    if "image" in property_data:

        image_path = property_data["image"]

        if image_path and os.path.exists(image_path):

            img = Image(
                image_path,
                width=5*inch,
                height=3*inch
            )

            img.hAlign = "CENTER"

            story.append(img)

            story.append(Spacer(1, 15))

    # -------------------------
    # Property Details
    # -------------------------

    story.append(
        Paragraph(
            "<b>PROPERTY DETAILS</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            f"<b>Type:</b> {property_data['type']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>City:</b> {property_data['city']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Area:</b> {property_data['area']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>BHK:</b> {property_data['bhk']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Price:</b> ₹{property_data['price']:,}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Builder:</b> {property_data['builder']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Parking:</b> {property_data['parking']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Area:</b> {property_data['sqft']} Sq.ft",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    # -------------------------
    # Amenities
    # -------------------------

    story.append(
        Paragraph(
            "<b>AMENITIES</b>",
            heading
        )
    )

    for amenity in property_data["amenities"]:
        story.append(
            Paragraph(
                f"✔ {amenity}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 25))

    # -------------------------
    # Contact
    # -------------------------

    story.append(
        Paragraph(
            "<b>CONTACT US</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            "Dream Homes Real Estate",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "Phone : +91 9876543210",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "Email : sales@dreamhomes.com",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "Website : www.dreamhomes.com",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename