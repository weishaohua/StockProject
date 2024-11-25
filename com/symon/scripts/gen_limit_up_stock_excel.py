import os
import sys
import time

import pandas as pd

from com.symon.utils import common_utils

"""
根据涨停股票分析情绪周期
"""


def append_first_limit_up_stock(df, stock_dict, start_row, col):
    if stock_dict is None or len(stock_dict) <= 0:
        return

    num = 0
    for name in stock_dict:
        row = start_row + num
        # 如果新列不存在，先创建新列并设为 object 类型
        if col >= len(df.columns):
            df.insert(col, f'new_col_{col}', pd.Series([None] * len(df), dtype='object'))
        print(f'first_limit_up_stock,row_index={row}, col_index={col}, data={name}')
        df.at[row, df.columns[col]] = name
        num = num + 1


def append_continue_limit_up_stock(df, stock_dict):
    if df.empty:
        return

    if stock_dict is None or len(stock_dict) <= 0:
        return

    yesterday_limit_up_stock = df.iloc[:, -1]
    for index, value in yesterday_limit_up_stock.items():
        if pd.isnull(value):
            continue

        col_index = df.columns.get_loc(yesterday_limit_up_stock.name)
        if value in stock_dict:
            col_index = col_index + 1
            # 如果新列不存在，先创建新列并设为 object 类型
            if col_index >= len(df.columns):
                df.insert(col_index, f'new_col_{col_index}', pd.Series([None] * len(df), dtype='object'))
            print(f'continue_limit_up_stock,row_index={index}, col_index={col_index}, data={value}')
            df.at[index, df.columns[col_index]] = value
            stock_dict.remove(value)


if __name__ == '__main__':
    limit_up_stock_file_path = f"../crawler/ths/data/2024-涨停股票.csv"
    source_df = pd.read_csv(limit_up_stock_file_path, index_col=False)
    # 指定日期开始增量补数据
    start_date = common_utils.get_standard_date(time.time(), '%Y%m%d')

    if source_df.empty:
        print(f'limit_up_stock_file_path:{limit_up_stock_file_path} data is empty')
        sys.exit()
    grouped = source_df.groupby('涨停日期')

    write_file_path = f'../crawler/ths/data/2024-情绪周期分析.xlsx'
    if os.path.isfile(write_file_path):
        write_df = pd.read_excel(write_file_path)
        header = write_df.columns.tolist()
    else:
        write_df = pd.DataFrame()
        header = []

    start_row_index = write_df.shape[0]
    start_col_index = write_df.shape[1]
    print(f'start_row_index:{start_row_index}, start_col_index:{start_col_index}')

    for group_name, group_data in grouped:
        header.append(group_name)

        sorted_group_data = group_data.sort_values('首次涨停时间', ascending=True)
        stock_name_dict = []
        for stock_name in sorted_group_data['股票名称']:
            stock_name_dict.append(stock_name)

        append_continue_limit_up_stock(write_df, stock_name_dict)
        append_first_limit_up_stock(write_df, stock_name_dict, start_row_index, start_col_index)

        start_row_index = start_row_index + len(stock_name_dict)
        start_col_index = start_col_index + 1

    write_df.to_excel(write_file_path, index=False, header=header)


