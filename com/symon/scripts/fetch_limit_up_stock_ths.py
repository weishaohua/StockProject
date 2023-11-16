import pandas as pd
import csv
import datetime
from com.symon.crawler.ths import data_api as ths

"""
从同花顺抓取涨停股票
"""


if __name__ == '__main__':
    # limit_up_day = '2023-11-16'
    limit_up_day = str(datetime.date.today())
    # stock_data = ths.get_limit_up_pool_after_date(ths.get_first_trade_day("20230101"), 400)
    # df = pd.DataFrame(stock_data)
    # df.to_csv(f"../crawler/ths/data/2023-涨停股票.csv", encoding='utf-8', header=True, mode='w', index=False, quoting=csv.QUOTE_NONE)
    stock_data = ths.get_limit_up_pool_after_date(ths.get_first_trade_day(limit_up_day), 1)
    df = pd.DataFrame(stock_data)
    df.to_csv(f"../crawler/ths/data/2023-涨停股票.csv", encoding='utf-8', header=False, mode='a', index=False, quoting=csv.QUOTE_NONE)