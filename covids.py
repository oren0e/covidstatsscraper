#!/usr/bin/env python
import argparse


def top_10_with_israel(by: str, ascending: bool = False):
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import re
    import numpy as np
    pd.set_option('expand_frame_repr', False)  # To view all the variables in the console

    url = "https://coronavirus.jhu.edu/data/mortality"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html5lib")

    mytable = soup.select("td")
    updated_for = soup.select("strong")

    table_lst = [item.text for item in mytable]

    update_datetime = [item.text for item in updated_for][0]
    regex = r'^This page was '
    update_datetime = re.sub(regex,"",update_datetime)
    update_datetime = update_datetime[0].upper() + update_datetime[1:]

    d = {'country' : table_lst[0::5], 'confirmed' : table_lst[1::5],
         'deaths' : table_lst[2::5], 'case_fatality_pct' : table_lst[3::5], 'deaths_per_100k_pop' : table_lst[4::5]}

    df = pd.DataFrame(d)

    # fix types
    df['confirmed'] = df['confirmed'].apply(lambda x: re.sub(r',',"",x))
    df['confirmed'] = pd.to_numeric(df['confirmed'])

    df['deaths'] = df['deaths'].apply(lambda x: re.sub(r',',"",x))
    df['deaths'] = pd.to_numeric(df['deaths'])

    df['case_fatality_pct'] = df['case_fatality_pct'].apply(lambda x: re.sub(r'%',"",x))
    df['case_fatality_pct'] = pd.to_numeric(df['case_fatality_pct'])

    # replace missing values
    df['deaths_per_100k_pop'] = df['deaths_per_100k_pop'].replace(to_replace='nan', value=np.nan)
    df['deaths_per_100k_pop'] = pd.to_numeric(df['deaths_per_100k_pop'])

    temp_df = (df.sort_values(by=by, ascending=ascending)
               .reset_index()
               .drop('index', axis=1)
               .reset_index()
               .rename(columns={"index": "rank"})
               )
    df_israel = temp_df[temp_df['country'] == 'Israel']
    print('\n',update_datetime)
    result_df = pd.concat([temp_df.head(10), df_israel], axis=0)
    hide_index = [''] * len(result_df)
    result_df.index = hide_index
    return result_df


# CLI
# create the parser
parser = argparse.ArgumentParser(prog='covids',
                                 description='Get statistics for the COVID-19 virus for top 10 countries'
                                             ' with Israel along')

# arguments
parser.add_argument('statistic', metavar='statistic', type=str,
                    help='One of: [confirmed, deaths, case_fatality_pct, deaths_per_100k_pop]')
parser.add_argument('-asc', '--ascending', action='store_true',
                    help='an optional argument for displaying results in ascending order')

args = parser.parse_args()
print(top_10_with_israel(by=args.statistic, ascending=args.ascending))
