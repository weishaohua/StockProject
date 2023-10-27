import time
import requests
import pandas as pd

"""
东方财富相关api
"""

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


def save_data(write_data, file_name, header=True):
    df = pd.DataFrame(write_data)
    df.to_csv(file_name, encoding='utf-8', header=header, index=False, mode='a')


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
        print(f'fetch url:{url}')
        json_data = get_page(url=url)
        if len(json_data['data']['data']) == 0:
            break
        else:
            temp = get_data(json_data=json_data, stock_code=stock_code, stock_name=stock_name)
            if temp == '未获取到数据！':
                continue
            else:
                return temp


if __name__ == '__main__':
    date = get_standard_date(timestamp=time.time())
    df = pd.read_csv('../ths/data/20230103-涨停股票.csv', encoding='utf-8')
    filtered_df = df[df['涨停日期'] == '2023-10-26']
    step = 0
    for i in filtered_df[['股票代码', '股票名称']].values:
        goal_data = start_get(stock_code=i[0], stock_name=i[1])
        if step == 0:
            save_data(goal_data, f'../ths/data/20230103-涨停股票今日竞价数据.csv', True)
        else:
            save_data(goal_data, f'../ths/data/20230103-涨停股票今日竞价数据.csv', False)
        step = step + 1
