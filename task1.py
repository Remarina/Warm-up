"""
Из базы загружены заказы клиентов магазина в
форме двух pandas.DataFrame’ов: orders и order_lines.

orders:

OrderId,CustomerId,DateTime
5,583,2017-01-01 15:03:17
13,900,2019-02-05 05:02:59
69,19573,2018-11-03 23:59:59

order_lines:
ProductId,OrderId,Price
5873,5,3026.0
7265,5,573.0
9675,5,159.0
5873,6,2999.0
13,6,57.0

1. Постройте отчёт по популярным продуктами - функцию,
возвращающую pandas.DataFrame, где видны
 •   самые популярные за последний месяц продукты
 •   суммарная выручка по каждому такому продукту
 •   средний чек заказов, в которых есть такие продукты
"""


import pandas as pd
from datetime import datetime


def get_popular_products(orders_csv, order_lines_csv):

    # Исходные данные
    orders = pd.read_csv(orders_csv, parse_dates=['DateTime'], dtype={
                         'OrderId': pd.Int64Dtype(), 'CustomerId': pd.Int64Dtype()})
    order_lines = pd.read_csv(order_lines_csv, dtype={
        'ProductId': pd.Int64Dtype(), 'OrderId': pd.Int64Dtype()})
    order_table = order_lines.merge(orders, how='outer', on='OrderId')
    # order_table = order_lines.merge(orders, how='inner', on='OrderId')
    # print(order_table)

    # Итоговый отчет
    popular_products = pd.DataFrame(
        columns=['ProductId', 'TotalRevenue', 'AverageCheck'])

    # Условие выбора: заказы за последний месяц текущего года
    last_month = datetime.today().month - 1
    current_year = datetime.today().year
    time_condition = (order_table['DateTime'].dt.month == last_month) & (
        order_table['DateTime'].dt.year == current_year)

    # Самые популярные продукты за последний месяц
    popular_products_id = order_table.where(
        time_condition)['ProductId'].mode().astype('int')
    if popular_products_id.empty:
        # print('В предыдущем месяце заказов не было\n')
        return popular_products

    # Коды самых популярных продуктов
    popular_products['ProductId'] = popular_products_id
    popular_products = popular_products.set_index('ProductId')

    for ProductId in popular_products_id:

        # Суммарная выручка по популярному продукту
        # (за последний месяц)
        popular_products.loc[ProductId, 'TotalRevenue'] = order_table['Price'].where(
            (order_table['ProductId'] == ProductId) & time_condition).sum()

        # номера заказов, в которых есть популярные продукты
        # (aналогично выручке, данные приведены за последний месяц)
        orders_with_popular = order_table.where(
            (order_table['ProductId'] == ProductId) & time_condition)['OrderId'] \
            .dropna()

        # Cредний чек (за последний месяц)
        average_check = order_table.where(
            order_table['OrderId'].isin(orders_with_popular))['Price'].sum() \
            / len(orders_with_popular)
        popular_products.loc[ProductId, 'AverageCheck'] = average_check

    return popular_products
