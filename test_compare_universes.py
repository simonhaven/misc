import unittest
import pandas as pd
import numpy as np
import compare_universes as cu

class UniverseTest(unittest.TestCase):

    def setUp(self):
        self.test_universe1 = pd.DataFrame({
            'COUNTRY':   [  'US',     'US',    'US',  'US',    'US',  'UK',    'UK',    'UK',     'UK',    'UK',    'UK',    'FR',    'NZ',    'NZ',   'NZ',   'NZ',     'NZ'], 
            'AXIOMA_ID': [ 'ABC',    'DEF',   'XYZ', 'GHI',   'DEF', 'OOO',   'PPP',   'OOO',    'QQQ',   'ZZZ',   'UUU',   'ZEE',   'DUH',   'OHO',  'III',  'ERR',    'NOO'],
            'PRICE':     [  25.0,       33,     6.5,  12.5,   101.5,   7.5,    83.7,    40.4,    243.8,    99.9,    48.0,   100.0,    66.5,   271.4,  301.4,  76.76,    163.2],
            'TSO':       [400000, 20000000, 1000000, 80000, 2000000, 90000, 6198283, 5000000,  7298260, 2828282, 5474640, 1000000, 8000000, 5726371, 700000, 502500, 92829295],
            'RETURN':    [   3.0,     25.2,     7.8,   4.9,    -1.6,   4.4,   0.123,     0.0,     -3.4,     4.1,  -0.728,     8.0,     0.0,   -4.33,  -1.98,   -5.2,    -9.72],
            })

        self.test_universe2 = pd.DataFrame({
            'COUNTRY':   [  'US',     'US',  'US',    'US',  'UK',    'UK',     'UK',    'UK',    'UK',    'FR',    'NZ',    'NZ',   'NZ',     'NZ'], 
            'AXIOMA_ID': [ 'ABC',    'DEF', 'GHI',   'DEF', 'OOO',   'PPP',    'QQQ',   'ZZZ',   'UUU',   'ZEE',   'DUH',   'III',  'ERR',    'NOO'],
            'PRICE':     [  25.0,       33,  12.5,   101.5,   7.5,    83.7,    243.8,    99.9,    48.0,   100.0,    66.5,   301.4,  76.76,    163.2],
            'TSO':       [400000, 20000000, 80000, 2000000, 90000, 6198283,  7298260, 2828282, 5474640, 1000000, 8000000,  700000, 502500, 92829295],
            'RETURN':    [   3.0,     25.2,   4.9,    -1.6,   4.4,   0.123,     -3.4,     4.1,  -0.728,     8.0,     0.0,   -1.98,   -5.2,    -9.72],
            })

    def test_largest_returns(self):
        expected_positive_results= { 'US': pd.DataFrame({'AXIOMA_ID':['DEF','XYZ','GHI'],'RETURN':[25.2, 7.8, 4.9]}),
                                     'UK': pd.DataFrame({'AXIOMA_ID':['OOO','ZZZ','PPP'],'RETURN':[4.4, 4.1, 0.123]}),
                                     'FR': pd.DataFrame({'AXIOMA_ID':['ZEE'],'RETURN':[8.0]}),
                                     'NZ': pd.DataFrame({'AXIOMA_ID':[],'RETURN':[]}) }

        expected_negative_results= { 'US':pd.DataFrame({'AXIOMA_ID':['DEF'],'RETURN':[-1.6]}),
                                     'UK':pd.DataFrame({'AXIOMA_ID':['QQQ','UUU'],'RETURN':[-3.4,-0.728]}),
                                     'FR':pd.DataFrame({'AXIOMA_ID':[],'RETURN':[]}),
                                     'NZ':pd.DataFrame({'AXIOMA_ID':['NOO','ERR','OHO'],'RETURN':[-9.72, -5.2, -4.33]}) }

        test_universe = self.test_universe1

        for country in expected_positive_results:
           
            print(f"Testing positive & negative returns for country [{country}]")
            country_data = test_universe[test_universe['COUNTRY'] == country]
            (largest_positive_df, largest_negative_df) = cu.get_largest_returns_for_country(country_data)

            assert(np.array_equal(largest_positive_df.values, expected_positive_results[country].values))

            assert(np.array_equal(largest_negative_df.values, expected_negative_results[country].values))

    def test_largest_market_caps(self):

        expected_largest_mcaps = {'US': pd.DataFrame({'AXIOMA_ID':['DEF','DEF','ABC','XYZ','GHI'],'MARKET_CAP':[660000000, 203000000, 10000000, 6500000, 1000000]}),
                                  'UK': pd.DataFrame({'AXIOMA_ID':['QQQ','PPP','ZZZ','UUU','OOO'],'MARKET_CAP':[1779315788, 518796287, 282545372, 262782720, 202000000]}),
                                  'FR': pd.DataFrame({'AXIOMA_ID':['ZEE'],'MARKET_CAP':[100000000]}),
                                  'NZ': pd.DataFrame({'AXIOMA_ID':['NOO','OHO','DUH','III','ERR'],'MARKET_CAP':[15149740944, 1554137089, 532000000, 210980000, 38571900]})}

        test_universe = self.test_universe1

        for country in expected_largest_mcaps:
           
            print(f"Testing market caps for country [{country}]")
            country_data = test_universe[test_universe['COUNTRY'] == country]
            largest_mcaps_df = cu.get_largest_market_caps_for_country(country_data)
            largest_mcaps_df['MARKET_CAP'] = largest_mcaps_df['MARKET_CAP'].round(decimals = 2)
            assert(np.array_equal(largest_mcaps_df.values, expected_largest_mcaps[country].values))

    def test_distinct_asset_count(self):

        expected_count = 2 
        test_universe1 = self.test_universe1
        test_universe2 = self.test_universe2
        actual_count = cu.get_distinct_asset_count(test_universe1, test_universe2)
        self.assertEqual(expected_count, actual_count) 

if __name__ == '__main__':
    unittest.main()
