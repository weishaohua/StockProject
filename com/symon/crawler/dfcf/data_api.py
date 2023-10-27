import time
import requests
import pandas as pd

# 东方财富

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://quote.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_standard_date(timestamp, mode="%Y-%m-%d"):
    return time.strftime(mode, time.localtime(timestamp))


def save_data(data, file_name, header=True):
    data = pd.DataFrame(data)
    file_path = './集合竞价数据'
    data.to_csv(f'{file_path}\\{file_name}.csv', encoding='gbk', header=header, index=False, mode='a')


def get_page(url: str, data_mode='{'):
    return jquery_list(requests.get(url=url, headers=headers).text, data_mode=data_mode)


def jquery_list(jquery: str, data_mode='{'):
    reverse_mode = {'[': ']', '{': '}', '(': ')'}
    tail_str = jquery[-5:][::-1]
    return eval(jquery[jquery.index(data_mode): -tail_str.index(reverse_mode[data_mode])])


def get_data(json_data, stock_code, stock_name):
    jhjj_data = '未获取到数据！'
    for i in json_data['data']['data']:
        if 92500 <= i['t'] < 93000:
            jhjj_data = {'股票代码': [stock_code], '股票名称': [stock_name], '成交价': [i['p'] / 1000], '成交量(手数)': [i['v']],
                         '成交金额': [round(i['p'] * i['v'] / 10, 0)]}
    return jhjj_data


def start_get(stock_code, stock_name):
    if str(stock_code)[0] == '6':
        market = 1
    else:
        market = 0
    for page in range(3):
        url = "http://push2ex.eastmoney.com/getStockFenShi?pagesize=144&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj" \
              f"&cb=jQuery1124032472207483171633_1633697823102&pageindex={page}&id={stock_code}1&sort=1&" \
              f"ft=1&code={stock_code[:-3]}&market={market}&_={int(time.time() * 1000)}"
        json_data = get_page(url=url)
        if len(json_data['data']['data']) == 0:
            break
        else:
            temp = get_data(json_data=json_data, stock_code=stock_code, stock_name=stock_name)
            if temp == '未获取到数据！':
                continue
            else:
                return temp


date = get_standard_date(timestamp=time.time())
data = pd.read_csv('2023-06-08-个股.csv', encoding='gbk')
data = data[data['开盘价'] != '-']
step = 0
for i in data[['股票代码', '股票名称']].values:
    print(step)
    goal_data = start_get(stock_code=i[0], stock_name=i[1])
    if step == 0:
        save_data(data=goal_data, file_name=f'{date}集合竞价数据')
    else:
        save_data(data=goal_data, file_name=f'{date}集合竞价数据', header=False)
    step += 1