import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "malletbosses@gmail.com"
password = "bfpmbdnuoxeeaygr"


def start_up():
    schedule.every().minute.do(count_auctions)
    while True:
        schedule.run_pending()
        time.sleep(1)


def count_auctions():
    url = "https://auta.ch/aukcje/?phrase=giulia&brand=&production_date_from=&production_date_to=&run_from=&run_to="

    try:
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        auction_entries = html.find_all('div', class_='auction-entry')
        counter = 0
        for auction in auction_entries:
            counter += 1

        if counter >= 1:
            context = ssl.create_default_context()
            try:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()  # Can be omitted
                server.starttls(context=context)  # Secure the connection
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)

                server.sendmail(sender_email, "sh0ken4u@gmail.com", html.encode())

            except Exception as e:
                # Print any error messages to stdout
                print(e)
            finally:
                server.quit()


    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_up()
