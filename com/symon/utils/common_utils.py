import time


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
