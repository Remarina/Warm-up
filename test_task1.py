import task1
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal


class TestFunc(unittest.TestCase):

    def test_get_popular_products(self):

        # Несколько популярных продуктов
        result1 = pd.DataFrame(data={'TotalRevenue': [6052, 318],
                                     'AverageCheck': [3185, 1672],
                                     'ProductId': [5873, 9675]}).set_index('ProductId')
        assert_frame_equal(task1.get_popular_products(
            'orders_csv.csv', 'order_lines_csv.csv'), result1)

        # Ни одного популярного продукта
        result2 = pd.DataFrame(
            columns=['ProductId', 'TotalRevenue', 'AverageCheck'])
        assert_frame_equal(task1.get_popular_products(
            'orders_csv2.csv', 'order_lines_csv2.csv'), result2)

        # Один популярный продукт
        result3 = pd.DataFrame(data={'TotalRevenue': [9078],
                                     'AverageCheck': [2452.5],
                                     'ProductId': [5873]}, dtype='object').set_index('ProductId')
        assert_frame_equal(task1.get_popular_products(
            'orders_csv3.csv', 'order_lines_csv3.csv'), result3)


if __name__ == '__main__':
    unittest.main()
