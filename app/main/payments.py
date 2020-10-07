import app.main.config as config
import Adyen
from random import randint
from flask import json

'''
Send Payment Request to Adyen
'''

def adyen_payments(frontend_request):
	adyen = Adyen.Adyen()
	adyen.client.platform = 'test'
	adyen.client.xapikey = config.checkout_apikey
	
	payment_info = frontend_request.get_json()
	txvariant = payment_info["paymentMethod"]["type"]
	
	payments_request = {
		'amount': {
			'value': 12500,
			'currency': choose_currency(txvariant)
		},
		'channel': 'Web',
		'reference': "Aditya's Test Shop" + str(randint(0, 10000)),
		'shopperReference': "Aditya's Test Shop Shopper",
		'returnUrl': "http://localhost:8080/api/handleShopperRedirect",
		'countryCode': 'NL',
		'shopperLocale': "en_US",
		'merchantAccount': config.merchant_account
	}
	payments_request.update(payment_info)
	
	if txvariant == 'alipay':
		payments_request['countryCode'] = 'CN'
	
	elif 'klarna' in txvariant:
		payments_request['shopperEmail'] = "myEmail@adyen.com"
		payments_request['lineItems'] = [
			{
				'quantity': "1",
				'amountExcludingTax': "450",
				'taxPercentage': "1111",
				'description': "Sunglasses",
				'id': "Item #1",
				'taxAmount': "50",
				'amountIncludingTax': "500",
				'taxCategory': "High"
			},
			{
				'quantity': "1",
				'amountExcludingTax': "450",
				'taxPercentage': "1111",
				'description': "Headphones",
				'id': "Item #2",
				'taxAmount': "50",
				'amountIncludingTax': "500",
				'taxCategory': "High"
			}]
	elif txvariant == 'directEbanking' or txvariant == 'giropay':
		payments_request['countryCode'] = "DE"
	
	elif txvariant == 'dotpay':
		payments_request['countryCode'] = "PL"
	
	elif txvariant == 'scheme':
		payments_request['additionalData'] = {"allow3DS2": "true"}
		payments_request['origin'] = "http://localhost:8080"
	
	elif txvariant == 'ach' or txvariant == 'paypal':
		payments_request['countryCode'] = 'US'
	
	print("/payments request:\n" + str(payments_request))
	
	payments_response = adyen.checkout.payments(payments_request)
	
	print("/payments response:\n" + payments_response.raw_response.decode("UTF-8"))
	return remove_unnecessary_data(payments_response.raw_response)


def choose_currency(payment_method):
	if payment_method == "alipay":
		return "CNY"
	elif payment_method == "dotpay":
		return "PLN"
	elif payment_method == "boletobancario":
		return "BRL"
	elif payment_method == "ach" or payment_method == "paypal":
		return "USD"
	else:
		return "EUR"


# Custom payment error class
class PaymentError(Exception):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)
	

# Format response being passed back to frontend. Only leave resultCode and action
def remove_unnecessary_data(response):
	dict_response = json.loads(response)
	if "resultCode" in dict_response:
		new_response = {"resultCode": dict_response["resultCode"]}
		if "action" in dict_response:
			new_response["action"] = dict_response["action"]
		return json.dumps(new_response)
	else:
		raise PaymentError(response)
