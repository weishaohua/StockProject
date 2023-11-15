"""
东方财富抓取集合竞价数据
"""
import time
import pandas as pd

from com.symon.crawler.dfcf import data_api as dfcf
from com.symon.utils import common_utils

if __name__ == '__main__':
    limit_up_day = '2023-11-14'
    limit_up_day_jj = '2023-11-15'

    date = common_utils.get_standard_date(timestamp=time.time())
    df = pd.read_csv('../crawler/ths/data/2023-涨停股票.csv', encoding='utf-8')
    filtered_df = df[df['涨停日期'] == limit_up_day]
    step = 0
    all_stock = []
    for stock in filtered_df[['股票代码', '股票名称', '收盘价', '成交金额']].values:
        goal_data = dfcf.get_open_data(limit_day=limit_up_day_jj, stock=stock)
        all_stock.append(goal_data)
    all_stock.sort(key=lambda x: x['竞价涨幅'], reverse=True)
    # dfcf.save_data(all_stock, f'../crawler/ths/data/2023-昨日涨停股票今日竞价数据.csv', True, 'w', 'utf-8')
    dfcf.save_data(all_stock, f'../crawler/ths/data/2023-昨日涨停股票今日竞价数据.csv', False, 'a', 'utf-8')
