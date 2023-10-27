"""
东方财富抓取集合竞价数据
"""
import time
import pandas as pd

from com.symon.crawler.dfcf import data_api as dfcf
from com.symon.utils import common_utils

if __name__ == '__main__':
    date = common_utils.get_standard_date(timestamp=time.time())
    df = pd.read_csv('../crawler/ths/data/2023-涨停股票.csv', encoding='utf-8')
    filtered_df = df[df['涨停日期'] == '2023-10-26']
    step = 0
    all_stock = []
    for stock in filtered_df[['股票代码', '股票名称', '收盘价']].values:
        goal_data = dfcf.start_get(limit_day='2023-10-26', stock_code=stock[0], stock_name=stock[1], yesterday_price=stock[2])
        all_stock.append(goal_data)
    all_stock.sort(key=lambda x: x['竞价涨幅'], reverse=True)
    dfcf.save_data(all_stock, f'../crawler/ths/data/2023-昨日涨停股票今日竞价数据.csv', True, 'w', 'utf-8')
