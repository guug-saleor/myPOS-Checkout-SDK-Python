import sys, os
pt = os.getcwd().replace('tests', '')
sys.path.insert(1, pt)

import uuid

from IPC.Config import Config
from IPC.Purchase import Purchase
from IPC.Customer import Customer
from IPC.Cart import Cart

conf = Config()

conf.setIpcURL('https://www.mypos.eu/vmp/checkout-test')

# String
conf.setPrivateKey('''\
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
-----END RSA PRIVATE KEY-----\
''')

# File
conf.setPrivateKeyPath( pt+'/keys/test.store_private_key.pem' )

conf.setLang('EN')
conf.setSid('000000000000010')
conf.setWallet('61938166610')
conf.setKeyIndex(1)

req = Purchase(conf)
req.setCurrency('EUR')
req.setOrderID(str(uuid.uuid4()))

req.setUrlOk('https://devs.mypos.com/mypos.eu/trunk/public/vmp/checkout/client/ipcOk')
req.setUrlCancel('https://devs.mypos.com/mypos.eu/trunk/public/vmp/checkout/client/ipcNOk')
req.setUrlNotify('https://devs.mypos.com/mypos.eu/trunk/public/vmp/checkout/client/ipcNotify')

req.setPaymentParametersRequired(3)
req.setPaymentMethod(1)
req.setCardTokenRequest(0)

req.setNote('Some note')

cus = Customer()
cus.setEmail('name@website.com')
cus.setFirstName('John')
cus.setLastName('Smith')
cus.setPhone('+23568956958')
cus.setCountry('DEU')
cus.setCity('Hamburg')
cus.setZip('20095')
cus.setAddress('Kleine Bahnstr. 41')

cart = Cart()
cart.add('Hp Probook 6360b Sticker', 2, 10.00, type=Cart.ITEM_TYPE_ARTICLE)
cart.add('Delivery Fee', 1, 3.45, type=Cart.ITEM_TYPE_DELIVERY)

req.setCustomer(cus)
req.setCart(cart)

print( req.process() )