import sys
import pandas as pd

def get_largest_returns_for_country(country_df):

        largest_positive = country_df[country_df['RETURN'] > 0].nlargest(3, 'RETURN')
        largest_negative = country_df[country_df['RETURN'] < 0].nsmallest(3, 'RETURN')
        return (largest_positive[['AXIOMA_ID','RETURN']], largest_negative[['AXIOMA_ID','RETURN']])
        
def get_largest_market_caps_for_country(country_df):

        country_df['MARKET_CAP'] = country_df['TSO'] * country_df['PRICE']
        largest_market_caps = country_df[country_df['MARKET_CAP'] > 0].nlargest(5, 'MARKET_CAP').round(0)
        return largest_market_caps[['AXIOMA_ID','MARKET_CAP']]
        
def compare_by_country(univ_df):
        country_list = univ_df['COUNTRY'].unique()
        for country in country_list:
            print(f"\nCountry: {country}")
            country_df = univ_df[univ_df['COUNTRY'] == country]
            (largest_positive, largest_negative) = get_largest_returns_for_country(country_df)
            largest_market_caps = get_largest_market_caps_for_country(country_df)
            print("Largest positive returns:")
            if len(largest_positive) > 0:
                print(largest_positive.to_string(index=False))
            else:
                print("None")
            print("Largest negative returns:")
            if len(largest_negative) > 0:
                print(largest_negative.to_string(index=False))
            else:
                print("None")
            print("Largest market caps:")
            if len(largest_market_caps) > 0:
                print(largest_market_caps.to_string(index=False))
            else:
                print("None")


def get_distinct_asset_count(univ1_df, univ2_df):
        return len(set(univ1_df['AXIOMA_ID'].unique()) - set(univ2_df['AXIOMA_ID'].unique()))

def compare_universes(universe1, universe2):

        print("\n\nLargest returns and market caps for universe 1:")
        compare_by_country(universe1)
        print("\n\nLargest returns and market caps for universe 2:")
        compare_by_country(universe2)
        
        distinct_asset_count = get_distinct_asset_count(universe1, universe2)
        print(f"\n\nDistinct assets in universe1 but not in universe2: {distinct_asset_count}")



if __name__ == '__main__':
     
        universe1_path = sys.argv[1]
        universe2_path = sys.argv[2]
        print(f" Comparing universe 1 [{universe1_path}] with universe 2 [{universe2_path}]")
        universe1 = pd.read_csv(universe1_path)
        universe2 = pd.read_csv(universe2_path)
        compare_universes(universe1, universe2)
