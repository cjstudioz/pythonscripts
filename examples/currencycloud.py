import requests

BASEURL = 'https://api.currencycloud.com/v2/' #'https://devapi.currencycloud.com/v2/'

session = requests.Session()
auth_resp = session.post(BASEURL+'authenticate/api', {
    'login_id': 'finatext_rates',
    'api_key': '5ed9b570d7f7228f060458dbb37a89a741af832c7e42ebf98ffc46b0988a77e4'
})

if auth_resp.status_code == 200:
    session.headers['X-Auth-Token'] = auth_resp.json()['auth_token']
else:
    raise RuntimeError(f'Error authenticating http error code: {auth_resp.status_code}')


response = session.get(BASEURL+'rates/find', params=dict(
    currency_pair='GBPUSD',
))

response.json()