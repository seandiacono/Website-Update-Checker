# A script to check whether the content of a website has been updated

from email import message
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

while True:
    url = Request('https://www.svenskfotboll.se/biljett/',
                  headers={'User-Agent': 'Mozilla/5.0'})

    current_response = urlopen(url).read()

    try:
        with open('last_response.txt', 'r', encoding='ISO-8859-1') as f:
            last_response = f.read()
    except FileNotFoundError:
        print('File not yet created')

    response_soup = BeautifulSoup(current_response, 'html.parser')

    ticket_info = response_soup.find_all('p', class_='banner__preamble')[1]

    if str(ticket_info) != last_response:
        message = client.messages.create(
            body='Ticket info has been updated', from_='+18064041704', to='+35699059592')
        print(message.sid)
        with open('last_response.txt', 'w', encoding='ISO-8859-1') as f:
            f.write(str(ticket_info))
    else:
        print('No changes')
