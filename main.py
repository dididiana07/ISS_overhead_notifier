import requests
import datetime as dt
from time import sleep
import smtplib


# CONSTANTS

MY_EMAIL = ""
PASSWORD = ""
RECIPIENT_EMAIL = ""

MY_LATITUDE = 41.917179
MY_LONGITUDE = 3.163800


def sunset_sunrise(lat, lng):
    """Returns a tuple with the hour the sun rises and the sun sets depending on your latitude and longitude."""
    parameters = {
        "lat": lat,
        "lng": lng,
        "formatted": 0
    }
    sunset_sunrise_response = requests.request("GET", "https://api.sunrise-sunset.org/json", params=parameters).json()
    sunrise_time = int(sunset_sunrise_response["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time = int(sunset_sunrise_response["results"]["sunset"].split("T")[1].split(":")[0])
    return sunrise_time, sunset_time


def is_iss_overhead(latitude, longitude):
    """Returns True if the ISS is near your location."""
    iss_response = requests.request("GET", "http://api.open-notify.org/iss-now.json").json()
    current_iss_longitude = float(iss_response["iss_position"]["longitude"])
    current_iss_latitude = float(iss_response["iss_position"]["latitude"])
    if int(latitude - 5) <= current_iss_latitude <= int(latitude + 5) \
            and int(longitude - 5) <= current_iss_longitude <= int(longitude + 5):
        return True


def main():
    while True:
        sleep(60)
        current_hour = dt.datetime.now().hour
        sunset, sunrise = sunset_sunrise(lat=MY_LATITUDE, lng=MY_LONGITUDE)
        if current_hour >= sunset or current_hour <= sunrise:
            if is_iss_overhead(latitude=MY_LATITUDE, longitude=MY_LONGITUDE):
                with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
                    connection.starttls()
                    connection.login(user=MY_EMAIL, password=PASSWORD)
                    connection.sendmail(from_addr=MY_EMAIL,
                                        to_addrs=RECIPIENT_EMAIL,
                                        msg=f"Subject: Look Up!\n\nThe ISS is about to pass near you. Don't miss it!")


if __name__ == "__main__":
    main()


