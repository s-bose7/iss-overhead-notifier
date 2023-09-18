import requests
import smtplib
import time
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MY_LAT = 23.238022
MY_LONG = 88.709326

def issOverhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    lat = float(data["iss_position"]["latitude"])
    long = float(data["iss_position"]["longitude"])

    if(MY_LAT-5 <= lat <= MY_LAT+5) and (MY_LONG-5 <= long <= MY_LONG+5):
        return True 

def isNight():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    timenow = datetime.now().hour

    if(timenow >= sunset or timenow <= sunrise):
        return True

def sendmail():
    sender_email = os.getenv("SENDER_MAIL")
    reciver_email = os.getenv("RECIVER_MAIL")
    password = os.getenv("PASSWORD")
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=sender_email, password=password)
    msg = "subject:LOOK UP!!!\n\nThe international space station is your overhead!!"
    connection.sendmail(from_addr=sender_email, to_addrs=reciver_email, msg=msg)
    print(f"The iss has been spoted & email has been sent at {datetime.now()}")
    connection.close()

while(True):
    time.sleep(60)
    if(issOverhead() and isNight()):
        sendmail()
