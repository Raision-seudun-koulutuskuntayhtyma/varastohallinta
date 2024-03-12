import base64
import io
import smtplib
import time
import uuid
from datetime import datetime, timedelta
from email.message import EmailMessage

import pytz
from barcode import Code128, EAN13
from barcode.writer import ImageWriter
from django.conf import settings
from django.core.files.base import ContentFile

from .models import Settings_CustomUser, Settings
from .storage_settings import *

# ======================================================
# EMAIL ALERT

# https://betterdatascience.com/send-emails-with-python/
# https://www.letscodemore.com/blog/smtplib-smtpauthenticationerror-username-and-password-not-accepted/
def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body, subtype='html')
    msg['subject'] = subject

    msg['from'] = STORAGE_EMAIL
    msg['to'] = to

    server = smtplib.SMTP(EMAIL_SERVER, 587)
    server.starttls()
    server.login(STORAGE_EMAIL, EMAIL_PASS)
    server.send_message(msg)
    server.quit()


# END EMAIL ALERT
# ======================================================


# ===========================================
# FILE SAVE FUNCTION

mime_type_to_extension = {
    "image/jpeg": "jpg",
    "image/png": "png",
}

def parse_image_from_data_url(data_url: str) -> ContentFile:
    """
    Parse an image from data URL to a ContentFile.

    The data URL should have image data in jpeg or png format in the
    standard base64 encoded form.  Returns a ContentFile object with a
    randomly generated filename and the image content which is decoded
    from the data URL.
    """
    base64_data: str = ""
    ext: str = ""
    for mime_type in mime_type_to_extension:
        prefix = f"data:{mime_type};base64,"
        if data_url.startswith(prefix):
            base64_data = data_url[len(prefix):]
            ext = mime_type_to_extension[mime_type]
            break

    if not base64_data:
        data_url_prefix = data_url[:50] + "..."
        raise ValueError(f"Unsupported data URL: {data_url_prefix!r}")

    data = base64.b64decode(base64_data)
    filename = f"{int(time.time())}_{str(uuid.uuid4())[:8]}.{ext}"
    return ContentFile(data, name=filename)


# END FILE SAVE FUNCTION
# ==============================================


# GET RENTAL PAGE VIEW
def get_rental_events_page(user) -> str:
    # page = Settings.objects.get(set_name='rental_page_view')
    try:
        page = Settings_CustomUser.objects.filter(user=user).get(setting_name__set_name='rental_page_view')
        rental_page = page.set_value
    except:
        rental_page = RENTAL_PAGE_VIEW
    return rental_page


# =============================================
# FILTERS
# ---------------------------------------------
# Storage filter
# Filter is empty if user is superuser or management
def storage_f(user) -> dict:
    """Storage filter.
    Return: storage_id
        Filter is empty if user is superuser or management
    """
    # Filteroi storage nimen mukaan, jos käyttäjillä Superuser oikeus niin näytetään kaikki tapahtumat kaikista varastoista
    storage_filter = {}
    try:
        user_group = str(user.groups.get())
    except:
        user_group = ''

    if not user.is_superuser and user_group != 'management':
        storage_filter = { 'storage_id' : user.storage_id }
    return storage_filter


# Datarange filter
def start_date_filter(start, end) -> dict:
    """Datarange filter.
    
    Return: { 'start_date__range' : [start_date, end_date] }
    """
    if bool(start) & bool(end): # if rental_start and rental_end not NULL
        date_formated = datetime.strptime(start, '%Y-%m-%d') # Make format stringed date to datetime format
        start_date = pytz.utc.localize(date_formated) # Add localize into datetime date

        date_formated = datetime.strptime(end, '%Y-%m-%d') # Make format stringed date to datetime format
        end_date = pytz.utc.localize(date_formated) + timedelta(days=1) # Add 1 day to include this all last day to the list
        start_date_range = { 'start_date__range' : [start_date, end_date] }
    else:
        start_date_range = {} # start_date range is empty if request.GET is empty
    return start_date_range

# Ordering filter
def order_filter_switch(user) -> int:
    """Ordering filter
    Return: 1 or 0
    """
    try:
        get_ordering_name = Settings.objects.get(set_name='rental_page_ordering')
    except:
        get_ordering_name = Settings.objects.create(set_name='rental_page_ordering')

    try:
        get_ordering = Settings_CustomUser.objects.filter(user=user).get(setting_name=get_ordering_name)
    except:
        get_ordering = Settings_CustomUser.objects.create(setting_name=get_ordering_name, user=user, set_value=1)
    return int(get_ordering.set_value)

# Ordering field
def order_field(user) -> list:
    """Get ordering name from Settings table
    All possible fields are written in the storage_settings.py
    Return: list
        [0]: Goods table field name
        [1]: Same name in Finnish
    """
    try:
        get_order_field_name = Settings.objects.get(set_name='rental_page_field_ordering')
    except:
        get_order_field_name = Settings.objects.create(set_name='rental_page_field_ordering')

    try:
        get_order_field = Settings_CustomUser.objects.filter(user=user).get(setting_name=get_order_field_name)
    except:
        get_order_field = Settings_CustomUser.objects.create(setting_name=get_order_field_name, user=user, set_value=RENTAL_PAGE_ORDERING_FIELDS[0])

    order_field_key = list(RENTAL_PAGE_ORDERING_FIELDS_D.keys())[list(RENTAL_PAGE_ORDERING_FIELDS_D.values()).index(get_order_field.set_value)]
    # print('order_field_key', order_field_key)
    # print('RENTAL_PAGE_ORDERING_FIELDS_D[order_field_key]', RENTAL_PAGE_ORDERING_FIELDS_D[order_field_key])
    return [order_field_key, RENTAL_PAGE_ORDERING_FIELDS_D[order_field_key]]

# ---------------------------------------------
# END OF FILTERS
# =============================================



# =============================================
# BARCODE GENERATOR
# ---------------------------------------------

def barcode_gen(num, code):
    rv = io.BytesIO()
    # Code128(str(num), writer=SVGWriter()).write(rv) # To SVG
    Code128(str(code)+str(num), writer=ImageWriter()).write(rv)
    byte_data = base64.b64encode(rv.getvalue()).decode()
    # print(rv.getvalue())
    return byte_data

def barcode_gen_ean13(num):
    rv = io.BytesIO()
    # Code128(str(num), writer=SVGWriter()).write(rv) # To SVG
    EAN13(str(num), writer=ImageWriter()).write(rv)
    byte_data = base64.b64encode(rv.getvalue()).decode()
    # print(rv.getvalue())
    return byte_data

# ---------------------------------------------
# END OF BARCODE GENERATOR
# =============================================





