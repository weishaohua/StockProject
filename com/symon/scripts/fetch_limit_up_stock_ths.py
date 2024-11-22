import pandas as pd
import csv
import time
from com.symon.crawler.ths import data_api as ths
from com.symon.utils import common_utils

"""
从同花顺抓取涨停股票
"""


if __name__ == '__main__':
    # limit_up_day = '20231218'
    limit_up_day = common_utils.get_standard_date(time.time(), '%Y%m%d')
    # stock_data = ths.get_limit_up_pool_after_date(ths.get_first_trade_day("20240101"), 400)
    # df = pd.DataFrame(stock_data)
    # df.to_csv(f"../crawler/ths/data/2024-涨停股票.csv", encoding='utf-8', header=True, mode='w', index=False, quoting=csv.QUOTE_NONE)
    stock_data = ths.get_limit_up_pool_after_date(ths.get_first_trade_day(limit_up_day), 1)
    df = pd.DataFrame(stock_data)
    df.to_csv(f"../crawler/ths/data/2024-涨停股票.csv", encoding='utf-8', header=False, mode='a', index=False, quoting=csv.QUOTE_NONE)