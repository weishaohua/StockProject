import time
import requests
import pandas as pd

from com.symon.utils.common_utils import get_standard_date
from com.symon.utils.common_utils import reverse_calc_order_amount

"""
东方财富相关api
"""

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'http://quote.eastmoney.com/',
}


def save_data(write_data, file_name, header=True, mode='w', encoding='utf-8'):
    write_df = pd.DataFrame(write_data)
    write_df.to_csv(file_name, encoding=encoding, header=header, index=False, mode=mode)


def get_page(url: str, data_mode='{'):
    cookies = {
        'qgqp_b_id': '18f6524c10e6c79b69b063a671363a26',
        'st_si': '94482754426918',
        'websitepoptg_show_time': '1698067053765',
        'HAList': 'ty-0-300290-%u8363%u79D1%u79D1%u6280%2Cty-0-300663-%u79D1%u84DD%u8F6F%u4EF6%2Cty-0-300059-%u4E1C%u65B9%u8D22%u5BCC%2Cty-0-300164-%u901A%u6E90%u77F3%u6CB9',
        'st_asi': 'delete',
        'st_pvi': '07350352822435',
        # 'st_sp': '2023-09-13%2019%3A38%3A56',
        'st_sp': '2023-10-27%2019%3A38%3A56',
        'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
        'st_sn': 346,
        'st_psi': '20231027160226611-113200322732-5796321173'
    }
    return jquery_list(requests.get(url=url, headers=headers).text, data_mode=data_mode)


def jquery_list(jquery: str, data_mode='{'):
    reverse_mode = {'[': ']', '{': '}', '(': ')'}
    tail_str = jquery[-5:][::-1]
    return eval(jquery[jquery.index(data_mode): -tail_str.index(reverse_mode[data_mode])])


def extract_open_data(json_data, limit_day, stock):
    """
    解析开盘数据

    :param json_data:原始json数据
    :param limit_day:涨停日期
    :param stock:股票信息
    """
    stock_data = '未获取到数据！'
    for time_data in json_data['data']['data']:
        # 竞价数据，取最后一条数据
        if 92500 <= time_data['t'] < 93000:
            stock_data = {
                '涨停日期': limit_day,
                '股票代码': stock['股票代码'],
                '股票名称': stock['股票名称'],
                '涨停情况': stock['连板情况'],
                '开盘价(元)': time_data['p'] / 1000,
                '竞价涨幅': round(((time_data['p'] - float(stock['收盘价']) * 1000) / (float(stock['收盘价']) * 1000)) * 100, 2),
                '竞价成交量(手)': int(time_data['v']),
                '竞价金额(元)': int(time_data['p'] * time_data['v'] / 10),
                '竞价金额与昨日成交金额占比': "{:.2%}".format(round(int(time_data['p'] * time_data['v'] / 10) / reverse_calc_order_amount(stock['成交金额']), 2))
            }
            if stock.get("涨幅") is not None and stock["涨幅"] is not None:
                stock_data['昨日涨幅'] = stock["涨幅"]
    return stock_data


def extract_close_data(json_data, limit_day, stock):
    """
    解析收盘数据

    :param json_data:原始json数据
    :param limit_day:涨停日期
    :param stock:股票信息
    """
    stock_data = '未获取到数据！'
    for time_data in json_data['data']['data']:
        # 收盘数据，取第一条数据
        if 92500 <= time_data['t'] < 160000:
            stock_data = {
                '涨停日期': limit_day,
                '股票代码': stock['股票代码'],
                '股票名称': stock['股票名称'],
                '涨停情况': stock['连板情况'],
                '收盘价(元)': time_data['p'] / 1000,
                '今日涨幅': round(((time_data['p'] - float(stock['收盘价']) * 1000) / (float(stock['收盘价']) * 1000)) * 100, 2)
            }
            break
    return stock_data


def get_open_data(limit_day, stock):
    """
    获取竞价开盘数据

    :param limit_day: 涨停日期
    :param stock: 涨停股票信息
    """
    # 分时正序
    sort = 1
    stock_code = stock['股票代码']
    if str(stock_code)[0] == '6':
        market = 1
    else:
        market = 0
    for page in range(3):
        url = "http://push2ex.eastmoney.com/getStockFenShi?pagesize=144&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj" \
              f"&cb=jQuery1124032472207483171633_1633697823102&pageindex={page}&id={stock_code}1&sort={sort}&" \
              f"ft=1&code={stock_code[:-3]}&market={market}&_={int(time.time() * 1000)}"
        print(f'fetch url:{url}')
        json_data = get_page(url=url)
        if len(json_data['data']['data']) == 0:
            break
        else:
            temp = extract_open_data(json_data=json_data, limit_day=limit_day, stock=stock)
            if temp == '未获取到数据！':
                continue
            else:
                return temp


def get_close_data(limit_day, stock):
    """
    获取收盘数据

    :param limit_day: 涨停日期
    :param stock: 涨停股票信息
    """
    # 分时倒序
    sort = 2
    stock_code = stock['股票代码']
    if str(stock_code)[0] == '6':
        market = 1
    else:
        market = 0
    for page in range(3):
        url = "http://push2ex.eastmoney.com/getStockFenShi?pagesize=144&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj" \
              f"&cb=jQuery1124032472207483171633_1633697823102&pageindex={page}&id={stock_code}1&sort={sort}&" \
              f"ft=1&code={stock_code[:-3]}&market={market}&_={int(time.time() * 1000)}"
        print(f'fetch url:{url}')
        json_data = get_page(url=url)
        if len(json_data['data']['data']) == 0:
            break
        else:
            temp = extract_close_data(json_data=json_data, limit_day=limit_day, stock=stock)
            if temp == '未获取到数据！':
                continue
            else:
                return temp


if __name__ == '__main__':
    date = get_standard_date(timestamp=time.time())
    df = pd.read_csv('../ths/data/2023-涨停股票.csv', encoding='utf-8')
    filtered_df = df[df['涨停日期'] == '2023-10-26']
    step = 0
    all_stock = []
    for stock in filtered_df[['股票代码', '股票名称', '收盘价', '成交金额']].values:
        goal_data = get_open_data(limit_day='2023-10-26', stock=stock)
        all_stock.append(goal_data)
    all_stock.sort(key=lambda x: x['竞价涨幅'], reverse=True)
    save_data(all_stock, f'../ths/data/2023-昨日涨停股票今日竞价数据.csv', True, 'w', 'utf-8')
