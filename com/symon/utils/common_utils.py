import time
from datetime import datetime

"""
通用工具类
"""


def is_st_stock(stock_name):
    """
    是否ST股票

    :param stock_name: 股票名称
    :return: true：是st股票，false：不是
    """
    return stock_name[:2] == "ST" or stock_name[:3] == "*ST"


def convert_stock_code(stock_code):
    """
    转换股票code格式

    :param stock_code: 原始股票code
    :return: 统一股票code
    """
    if stock_code.startswith("30"):
        return stock_code + ".CY"
    elif stock_code.startswith("688"):
        return stock_code + ".KC"
    elif stock_code.startswith("60"):
        return stock_code + ".SH"
    elif stock_code.startswith("00"):
        return stock_code + ".SZ"
    elif stock_code.startswith("8"):
        return stock_code + ".BJ"
    else:
        return "未知"


def second_to_date(timestamp):
    """
    秒时间戳转时间

    :param timestamp: 时间戳，单位秒
    :return: 时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def millisecond_to_date(timestamp):
    """
    毫秒时间戳转时间

    :param timestamp: 时间戳，单位毫秒
    :return: 时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000))


def get_standard_date(timestamp, mode="%Y-%m-%d"):
    """
    指定格式获取时间字符串

    :param timestamp: 时间戳
    :param mode: 指定输出格式
    :return: 时间字符串
    """
    return time.strftime(mode, time.localtime(timestamp))


def calc_order_volume(order_volume):
    """
    计算封单量单位

    :param order_volume: 封单股数
    """
    if order_volume <= 1000000:
        volume = round(order_volume / 100 / 10000, 3)
    elif order_volume <= 10000000:
        volume = round(order_volume / 100 / 10000, 2)
    elif order_volume < 100000000:
        volume = round(order_volume / 100 / 10000, 1)
    else:
        volume = int(order_volume / 100000000)
    return volume


def calc_order_amount(order_amount):
    """
    计算封单金额单位

    :param order_amount: 封单金额(元)
    """
    if order_amount <= 100000:
        amount = f'{round(order_amount / 10000, 3)}万'
    elif order_amount < 1000000:
        amount = f'{round(order_amount / 10000, 2)}万'
    elif order_amount < 10000000:
        amount = f'{round(order_amount / 10000, 1)}万'
    elif order_amount < 100000000:
        amount = f'{int(order_amount / 10000)}万'
    elif order_amount < 1000000000:
        amount = f'{round(order_amount / 100000000, 3)}亿'
    elif order_amount < 10000000000:
        amount = f'{round(order_amount / 100000000, 2)}亿'
    elif order_amount < 100000000000:
        amount = f'{round(order_amount / 100000000, 1)}亿'
    else:
        amount = f'{int(order_amount / 100000000)}亿'
    return amount


def reverse_calc_order_amount(order_amount):
    """
    计算金额单位还原成元

    :param order_amount: 封单金额
    """
    if order_amount.endswith('万'):
        amount = int(float(order_amount[0:-1]) * 10000)
    elif order_amount.endswith('亿'):
        amount = int(float(order_amount[0:-1]) * 100000000)
    else:
        amount = None
    return amount


if __name__ == '__main__':
    print(reverse_calc_order_amount("9.03亿"))
