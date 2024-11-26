"""
东方财富抓取昨日涨停今天集合竞价和收盘数据
"""
import sys
import time
import pandas as pd
import datetime

from com.symon.crawler.dfcf import data_api as dfcf
from com.symon.utils import common_utils

if __name__ == '__main__':
    # limit_up_day = '2024-11-22'
    # limit_up_day_jj = '2024-11-25'
    limit_up_day = str(datetime.date.today() - datetime.timedelta(days=1))
    limit_up_day_jj = str(datetime.date.today())
    print(f'limit_up_day:{limit_up_day}, limit_up_day_jj:{limit_up_day_jj}')

    date = common_utils.get_standard_date(timestamp=time.time())
    df = pd.read_csv('../crawler/ths/data/2024-涨停股票.csv', encoding='utf-8')
    filtered_df = df[df['涨停日期'] == limit_up_day]
    step = 0
    all_stock = []
    for stock_code, stock_name, yesterday_close_price, yesterday_amount, continue_limit_up in filtered_df[['股票代码', '股票名称', '收盘价', '成交金额', '连板情况']].values:
        stock = {
            '股票代码': stock_code,
            '股票名称': stock_name,
            '收盘价': yesterday_close_price,
            '成交金额': yesterday_amount,
            '连板情况': continue_limit_up
        }
        stock_open_data = dfcf.get_open_data(limit_day=limit_up_day_jj, stock=stock)
        stock_close_data = dfcf.get_close_data(limit_day=limit_up_day_jj, stock=stock)
        if stock_open_data is None or stock_close_data is None:
            print(f"get data failed, stock_open_data:{stock_open_data}, stock_close_data:{stock_close_data}")
            sys.exit()
        stock_open_close_data = {}
        stock_open_close_data.update(stock_open_data)
        stock_open_close_data.update(stock_close_data)
        all_stock.append(stock_open_close_data)
    all_stock.sort(key=lambda x: x['竞价涨幅'], reverse=True)
    dfcf.save_data(all_stock, f'../crawler/ths/data/2024-昨日涨停股票今日竞价和收盘数据.csv', True, 'w', 'utf-8')
    # dfcf.save_data(all_stock, f'../crawler/ths/data/2024-昨日涨停股票今日竞价和收盘数据.csv', False, 'a', 'utf-8')
