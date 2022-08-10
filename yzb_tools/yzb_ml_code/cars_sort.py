import requests
import logging

def get_token():
    api_key = '8PUghUN3aX8M7a0HwL5DF0L0'
    secret_key = '1Skr7sm2oGDqU0PSBCuNvQPStM2y0n5v'

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(api_key,secret_key)
    response = requests.get(host)
    if response:
        # print(response.json())
        return response.json()['access_token']


def main(access_token,text):
    try:
        request_url = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_cls/cars_sort'

        params = "{\"text\":\""+text+"\"}"

        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers).json()
        print(response,'==============')
        if response:
            result = response['results'][0]['name']
            return result
    except Exception as e:
        logging.exception(e)



# if __name__ == '__main__':
#     # print(get_token())
#     access_token = get_token()
#     text = '重庆市南岸区各街镇卫生院救护车采购(20A00414,20A00400,20A00418,20A00420,20A00389,20A00416)结果公告'.encode('utf8').decode('latin-1')
#     print(text)
#     print(main(access_token,text))
