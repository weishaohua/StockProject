import pandas as pd
import csv
from com.symon.crawler.ths import data_api as ths

"""
从同花顺抓取涨停/炸板/跌停股票
"""


if __name__ == '__main__':
    # stock_data = ths.get_limit_up_pool_after_date(ths.get_first_trade_day("20230101"), 300)
    # df = pd.DataFrame(stock_data)
    # df.to_csv(f"../crawler/ths/data/2023-涨停股票.csv", encoding='utf-8', header=True, mode='w', index=False, quoting=csv.QUOTE_NONE)
    # limit_up_stock_data = ths.get_limit_up_pool_after_date(ths.get_first_trade_day("20231027"), 1)
    open_limit_stock_data = ths.get_open_limit_pool_after_date(ths.get_first_trade_day("20231027"), 1)
    df = pd.DataFrame(open_limit_stock_data)
    df.to_csv(f"../crawler/ths/data/2023-涨停-炸板-跌停-股票.csv", encoding='utf-8', header=True, mode='w', index=False, quoting=csv.QUOTE_NONE)