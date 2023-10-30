from datetime import datetime

from com.symon.utils import common_utils
from com.symon.utils.httpclient import requests_utils
import json

"""
同花顺相关api
"""


def get_limit_up_pool(page, limit, date):
    """
    获取涨停股票

    :param page: 第几页
    :param limit: 每页多少条记录
    :param date: 日期，格式'%Y%m%d'
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool?page={page}&limit={limit}&field=19,199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,9003,9004&filter=HS,GEM2STAR&order_field=330324&order_type=1&date={date}&_={datetime.now().timestamp()}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_lower_limit_pool(page, limit, date):
    """
    获取跌停股票

    :param page: 第几页
    :param limit: 每页多少条记录
    :param date: 日期，格式'%Y%m%d'
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/lower_limit_pool?page={page}&limit={limit}&field=199112,10,330333,330334,1968584,3475914,9004&filter=HS,GEM2STAR&order_field=330334&order_type=0&date={date}&_={datetime.now().timestamp()}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_continuous_limit_pool(page, limit, date):
    """
    获取连板股票

    :param page: 第几页
    :param limit: 每页多少条记录
    :param date: 日期，格式'%Y%m%d'
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_pool?page={page}&limit={limit}&field=199112,10,330329,330325,133971,133970,1968584,3475914,3541450,9004&filter=HS,GEM2STAR&order_field=330329&order_type=0&date={date}&_={datetime.now().timestamp()}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_continuous_limit_up(date):
    """
    获取连板股票

    :param date: 日期，格式'%Y%m%d'
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_up?filter=HS,GEM2STAR&date={date}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_open_limit_pool(page, limit, date):
    """
    获取炸板股票

    :param page: 第几页
    :param limit: 每页多少条记录
    :param date: 日期，格式'%Y%m%d'
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/open_limit_pool?page={page}&limit={limit}&field=199112,9002,48,1968584,19,3475914,9003,10,9004,9001,330323,330324,330325,330329,133971,133970&filter=HS,GEM2STAR&order_field=199112&order_type=0&date={date}&_={datetime.now().timestamp()}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_limit_up(page, limit, date):
    """
    获取冲刺涨停股票

    :param page: 第几页
    :param limit: 每页多少条记录
    :param date: 日期，格式'%Y%m%d'
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/limit_up?page={page}&limit={limit}&field=199112,10,48,1968584,19,3475914,9003,9004&filter=HS,GEM2STAR&order_field=199112&order_type=0&date={date}&_={datetime.now().timestamp()}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_block_top(date):
    """
    最强风口

    :param date: 日期，格式'%Y%m%d'
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/block_top?filter=HS,GEM2STAR&date={date}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_trade_status():
    """
    判断当前日期是否交易日

    """
    url = "https://data.10jqka.com.cn/dataapi/limit_up/v1/trade_status"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_trade_day(date, next_days, prev_days):
    """
    获取交易日期

    :param date: 日期，格式'%Y%m%d'
    :param next_days: 后面多少个交易日
    :param prev_days: 前面多少个交易日
    """
    url = f"https://data.10jqka.com.cn/dataapi/limit_up/trade_day?date={date}&stock=stock&next={next_days}&prev={prev_days}"
    return requests_utils.get(url, headers=build_headers(), timeout=5)


def get_first_trade_day(date):
    """
    获取指定日期后第一个交易日期，包含当前日期

    :param date: 日期，格式'%Y%m%d'
    """
    trade_day = get_trade_day(date, 1, 1)
    data = json.loads(trade_day)["data"]
    is_trade_day = data["trade_day"]
    if is_trade_day:
        return str(date)
    else:
        return data["next_dates"][0]


def get_limit_up_pool_after_date(date, limit_day=1):
    """
    获取指定日期之后的所有涨停股票

    :param date: 日期，格式'%Y%m%d'
    :param limit_day: 获取几个交易日的数据，默认1天
    """
    first_trade_day = get_first_trade_day(date)
    now_trade_day = get_first_trade_day(datetime.now().strftime("%Y%m%d"))

    trade_day_array = [first_trade_day]
    while datetime.strptime(first_trade_day, "%Y%m%d").date() < datetime.strptime(now_trade_day, "%Y%m%d").date() and limit_day > len(trade_day_array):
        next_dates = json.loads(get_trade_day(first_trade_day, 30, 1))["data"]["next_dates"]
        trade_day_array.extend(next_dates[:limit_day - len(trade_day_array)])
        first_trade_day = next_dates[-1]

    limit_up_all = []
    for day in trade_day_array:
        page = 1
        limit_up_pool = json.loads(get_limit_up_pool(page, 50, day))
        limit_up_data = limit_up_pool["data"]["info"]
        limit_up_all.extend(build_stock_data(limit_up_data))

        page_info = limit_up_pool["data"]["page"]
        print(f"fetch day:{day},page:{page},page_info:{page_info}")
        while page_info["page"] < page_info["count"]:
            page += 1
            limit_up_pool = json.loads(get_limit_up_pool(page, 50, day))
            limit_up_data = limit_up_pool["data"]["info"]
            page_info = limit_up_pool["data"]["page"]
            limit_up_all.extend(build_stock_data(limit_up_data))
            print(f"fetch day:{day},page:{page},page_info:{page_info}")

    return limit_up_all


def get_open_limit_pool_after_date(date, limit_day=1):
    """
    获取指定日期之后的所有炸板股票

    :param date: 日期，格式'%Y%m%d'
    :param limit_day: 获取几个交易日的数据，默认1天
    """
    first_trade_day = get_first_trade_day(date)
    now_trade_day = get_first_trade_day(datetime.now().strftime("%Y%m%d"))

    trade_day_array = [first_trade_day]
    while datetime.strptime(first_trade_day, "%Y%m%d").date() < datetime.strptime(now_trade_day, "%Y%m%d").date() and limit_day > len(trade_day_array):
        next_dates = json.loads(get_trade_day(first_trade_day, 30, 1))["data"]["next_dates"]
        trade_day_array.extend(next_dates[:limit_day - len(trade_day_array)])
        first_trade_day = next_dates[-1]

    open_limit_all = []
    for day in trade_day_array:
        page = 1
        open_limit_pool = json.loads(get_open_limit_pool(page, 50, day))
        open_limit_data = open_limit_pool["data"]["info"]
        open_limit_all.extend(build_stock_data(open_limit_data))

        page_info = open_limit_pool["data"]["page"]
        print(f"fetch day:{day},page:{page},page_info:{page_info}")
        while page_info["page"] < page_info["count"]:
            page += 1
            open_limit_pool = json.loads(get_open_limit_pool(page, 50, day))
            open_limit_data = open_limit_pool["data"]["info"]
            page_info = open_limit_pool["data"]["page"]
            open_limit_all.extend(build_stock_data(open_limit_data))
            print(f"fetch day:{day},page:{page},page_info:{page_info}")

    return open_limit_all


def build_stock_data(stock_data):
    """
    封装数据

    :param stock_data: 数据集合
    :return: 封装后的数据集合
    """
    limit_up_all = []
    for stock in stock_data:
        data = {
            '涨停日期': common_utils.get_standard_date(int(stock["first_limit_up_time"])),
            '股票代码': f'{common_utils.convert_stock_code(stock["code"])}',
            '股票名称': stock["name"],
            '收盘价': stock["latest"],
            '首次涨停时间': common_utils.get_standard_date(int(stock["first_limit_up_time"]), '%H:%m:%S'),
            '最后涨停时间': common_utils.get_standard_date(int(stock["last_limit_up_time"]), '%H:%m:%S'),
            '连板情况': stock["high_days"],
            '是否连板': int(stock["is_again_limit"]),
            '涨停类型': stock["limit_up_type"],
            '涨停原因': stock["reason_type"],
            '成交金额': common_utils.calc_order_amount(stock["turnover"]),
            '换手率': round(stock["turnover_rate"], 2),
            '封单额': common_utils.calc_order_amount(stock["order_amount"]),
            '封单量': f'{common_utils.calc_order_volume(stock["order_volume"])}万手',
            '涨幅': round(stock["change_rate"], 2),
            '流通市值': f'{int(stock["currency_value"] / 100000000)}亿'
        }
        if stock["open_num"] is not None:
            data['开板次数'] = int(stock["open_num"])
        data['是否新股'] = stock["is_new"]
        if stock["limit_up_suc_rate"] is not None:
            data['近一年涨停封板率'] = round(stock["limit_up_suc_rate"], 2)
        limit_up_all.append(data)
        limit_up_all.sort(key=lambda x: x['首次涨停时间'], reverse=False)
    return limit_up_all


def build_headers():
    """
    构建请求头信息
    """
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'data.10jqka.com.cn',
        # 'Cookie': 'v=A8GndDMWQe4CYqwNmPdIHydT1gbe7jepX2PZ9CMWvj4nEu94az5FsO-y622w',
        'Referer': 'https://data.10jqka.com.cn/datacenterph/limitup/limtupInfo.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/116.0.0.0 Safari/537.36 '
    }
    return headers


if __name__ == '__main__':
    print(get_limit_up_pool(1, 15, '20231012'))
    print(get_lower_limit_pool(1, 15, '20231012'))
    print(get_continuous_limit_pool(1, 15, '20231013'))
    print(get_open_limit_pool(1, 15, '20231013'))
    print(get_limit_up(1, 15, '20231013'))
    print(get_continuous_limit_up('20231013'))
    print(get_block_top('20231013'))
    print(get_trade_status())
    print(get_trade_day('20231021', 2, 2))
    print(get_limit_up_pool_after_date('20231018', 2))
