#!/usr/bin/env python
from core_files.backend import Covid
import argparse

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
parser.add_argument('-csv', '--csv', action='store',
                    help='an optional argument to save as csv file: -csv [path]')
args = parser.parse_args()

if args.statistic is None:
    pass
else:
    if args.csv is not None:
        covd = Covid(by=args.statistic, ascending=args.ascending)
        covd.write_to_csv(path=args.csv)
    else:
        covd = Covid(by=args.statistic, ascending=args.ascending)
        print(covd.top_10_table())
