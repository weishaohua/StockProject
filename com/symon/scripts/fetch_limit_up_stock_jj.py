"""
东方财富抓取集合竞价数据
"""
import datetime
import pandas as pd

from com.symon.crawler.dfcf import data_api as dfcf

if __name__ == '__main__':
    # limit_up_day = '2023-11-16'
    # limit_up_day_jj = '2023-11-17'
    limit_up_day = str(datetime.date.today() - datetime.timedelta(days=1))
    limit_up_day_jj = str(datetime.date.today())

    df = pd.read_csv('../crawler/ths/data/2023-涨停股票.csv', encoding='utf-8')
    filtered_df = df[df['涨停日期'] == limit_up_day]
    step = 0
    all_stock = []
    total = 0
    for stock_code, stock_name, yesterday_close_price, yesterday_amount in filtered_df[['股票代码', '股票名称', '收盘价', '成交金额']].values:
        stock = {
            '股票代码': stock_code,
            '股票名称': stock_name,
            '收盘价': yesterday_close_price,
            '成交金额': yesterday_amount
        }
        goal_data = dfcf.get_open_data(limit_day=limit_up_day_jj, stock=stock)
        all_stock.append(goal_data)
        total = total + 1
    all_stock.sort(key=lambda x: x['竞价涨幅'], reverse=True)
    # dfcf.save_data(all_stock, f'../crawler/ths/data/2023-昨日涨停股票今日竞价数据.csv', True, 'w', 'utf-8')
    dfcf.save_data(all_stock, f'../crawler/ths/data/2023-昨日涨停股票今日竞价数据.csv', False, 'a', 'utf-8')
    print(f"completed stock total:{total}")
