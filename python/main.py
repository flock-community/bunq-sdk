from fastapi import FastAPI
from lib.bunq_lib import BunqClient
from signing import sign_data
import os
import subprocess
import requests
import json

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"

bunq_client = BunqClient(USER_API_KEY, service_name='PeterScript')


# Run these 1x to initialize your application 
bunq_client.create_installation()
bunq_client.create_device_server()


bunq_client.create_session()

app = FastAPI()


@app.get("/get_cards")
def get_cards():
    response = bunq_client.request(endpoint='card',method='GET',data={})
    return response


@app.get("/monetary_account")
def get_monetary_account():
    response = bunq_client.request(endpoint='monetary-account',method='GET',data={})
    return response



@app.get("/request")
def request():
    endpoint = f"monetary-account/"
    response = bunq_client.request(endpoint=endpoint, method='GET', data=None)
    return response

@app.get("/payment")
def payment():
    payment = bunq_client.create_payment(
        amount='0.10', 
        recipient_iban='NL14RABO0169202917',
        currency='EUR',
        from_monetary_account_id='1989601', 
        description='test'
    )
    return payment
