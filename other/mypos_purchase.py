import json
import uuid

from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from flask import Flask

app = Flask(__name__)

_CHECKOUT_URL = 'https://www.mypos.eu/vmp/checkout-test'
_PRIVATE_KEY = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCf0TdcTuphb7X+Zwekt1XKEWZDczSGecfo6vQfqvraf5VPzcnJ
2Mc5J72HBm0u98EJHan+nle2WOZMVGItTa/2k1FRWwbt7iQ5dzDh5PEeZASg2UWe
hoR8L8MpNBqH6h7ZITwVTfRS4LsBvlEfT7Pzhm5YJKfM+CdzDM+L9WVEGwIDAQAB
AoGAYfKxwUtEbq8ulVrD3nnWhF+hk1k6KejdUq0dLYN29w8WjbCMKb9IaokmqWiQ
5iZGErYxh7G4BDP8AW/+M9HXM4oqm5SEkaxhbTlgks+E1s9dTpdFQvL76TvodqSy
l2E2BghVgLLgkdhRn9buaFzYta95JKfgyKGonNxsQA39PwECQQDKbG0Kp6KEkNgB
srCq3Cx2od5OfiPDG8g3RYZKx/O9dMy5CM160DwusVJpuywbpRhcWr3gkz0QgRMd
IRVwyxNbAkEAyh3sipmcgN7SD8xBG/MtBYPqWP1vxhSVYPfJzuPU3gS5MRJzQHBz
sVCLhTBY7hHSoqiqlqWYasi81JzBEwEuQQJBAKw9qGcZjyMH8JU5TDSGllr3jybx
FFMPj8TgJs346AB8ozqLL/ThvWPpxHttJbH8QAdNuyWdg6dIfVAa95h7Y+MCQEZg
jRDl1Bz7eWGO2c0Fq9OTz3IVLWpnmGwfW+HyaxizxFhV+FOj1GUVir9hylV7V0DU
QjIajyv/oeDWhFQ9wQECQCydhJ6NaNQOCZh+6QTrH3TC5MeBA1Yeipoe7+BhsLNr
cFG8s9sTxRnltcZl1dXaBSemvpNvBizn0Kzi8G3ZAgc=
-----END RSA PRIVATE KEY-----
'''

@app.route('/')
def purchase():
    purchase_data = dict(
        IPCMethod='IPCPurchase',
        IPCVersion='1.4',
        IPCLanguage='EN',
        SID='000000000000010',
        walletnumber='61938166610',
        Amount=23.45,
        Currency='EUR',
        OrderID=str(uuid.uuid4()),
        URL_OK='https://devs.mypos.com/mypos.eu/trunk/public/vmp/checkout/client/ipcOk',
        URL_Cancel='https://devs.mypos.com/mypos.eu/trunk/public/vmp/checkout/client/ipcNOk',
        URL_Notify='https://devs.mypos.com/mypos.eu/trunk/public/vmp/checkout/client/ipcNotify',
        CardTokenRequest=0,
        KeyIndex=1,
        PaymentParametersRequired=3,
        PaymentMethod=1,
        customeremail='name@website.com',
        customerfirstnames='John',
        customerfamilyname='Smith',
        customerphone='+23568956958',
        customercountry='DEU',
        customercity='Hamburg',
        customerzipcode='20095',
        customeraddress='Kleine Bahnstr. 41',
        note='Some note',
        CartItems=2,
        Article_1='HP ProBook 6360b sticker',
        Quantity_1=2,
        Price_1=10.00,
        Currency_1='EUR',
        Amount_1=20.00,
        Article_2='Delivery',
        Quantity_2=1,
        Price_2=3.45,
        Currency_2='EUR',
        Amount_2=3.45
    )
    purchase_data['Signature'] = _generate_signature(purchase_data)
    
    return _generate_html_form(purchase_data)

def _private_key():
    return _PRIVATE_KEY.replace('-----BEGIN RSA PRIVATE KEY-----', '').replace('-----END RSA PRIVATE KEY-----', '').replace('\n', '')

def _generate_signature(data):
    data_to_sign = '-'.join([str(item[1]) for item in data.items()])
    rsa_key = RSA.importKey(b64decode(_private_key()))
    signer = PKCS1_v1_5.new(rsa_key)
    digest = SHA256.new()
    digest.update(b64encode(data_to_sign.encode('utf-8')))
    sign = signer.sign(digest)
    return b64encode(sign).decode('utf-8')

def _generate_html_form(data):
    raw_html = '<html><body onload="document.ipcForm.submit()">'
    raw_html += '<form id="ipcForm" name="ipcForm" action="%s" method="post">' % _CHECKOUT_URL

    for item in data.items():
        raw_html += '<input type="hidden" name="%s" value="%s"/><br>' % item

    raw_html += '</form></body></html>'
    return raw_html

if __name__ == '__main__':
    app.run()