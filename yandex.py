import requests, logging, flask
from yandex_money.api import Wallet, ExternalPayment

client_id = 'C0FCBFFF08B1BFA8325EE66D083B97C127FADFE152597F69BB567E06DD302C6C'

method = 'https://yoomoney.ru/oauth/authorize HTTP/1.1'
ym_account = 'rojentsev.m@yandex.ru'
redirect_uri = 'https://www.google.com/'

# scope = ['account-info payment.to-account("%s").limit(,%s)' % ('4100112670410693', '10')]
# auth_url = Wallet.build_obtain_token_url(code1, redirect_uri, scope)
# return redirect(auth_url)

# scope = ['account-info payment.to-account("%s").limit(,%s)' % (ym_account, 10)]
# auth_url = Wallet.build_obtain_token_url(client_id, redirect_uri, scope) + '&response_type=code'
# token = Wallet.get_access_token(client_id=client_id,code=flask.request.args['code'],redirect_uri=auth_url)['access_token']


scope = ['payment-shop.limit(30,10000) money-source("4100 1126 7041 0693")'] # etc..
auth_url = Wallet.build_obtain_token_url(client_id, redirect_uri, scope) + '&response_type=code'
print(auth_url)
# token = Wallet.get_access_token(client_id=client_id, code=auth_url, redirect_uri=auth_url)['access_token']
# print(token)