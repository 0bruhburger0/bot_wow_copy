import requests, time


api_access_token = 'тут токен'
mylogin = 'номер кошелька'


### Достает рублевый баланc ###
def get_balance(login, api_access_token):
    s7 = requests.Session()
    s7.headers['Accept']= 'application/json'
    s7.headers['authorization'] = 'Bearer ' + api_access_token
    p = s7.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    balances = p.json()['accounts']
    rubAlias = [x for x in balances if x['alias'] == 'qw_wallet_rub']
    rubBalance = rubAlias[0]['balance']['amount'] # Баланс
    return rubBalance
# print(get_balance(mylogin, api_access_token))


### Платеж ###
def send_p2p(to_qw, comment, sum_p2p, api_access_token):
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + api_access_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    postjson = {"id": "", "sum": {"amount": "", "currency": ""}, "paymentMethod": {"type": "Account", "accountId": "643"}, "comment": "", "fields": {"account": ""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = sum_p2p
    postjson['sum']['currency'] = '643'
    postjson['fields']['account'] = to_qw
    postjson['comment'] = str(comment)
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json = postjson)
    print(res.text)

# print(send_p2p(api_access_token, '+79122658414', 'comment', 99.01))
