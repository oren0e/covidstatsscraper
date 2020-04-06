# COVID-19 (corona-virus) statistics scraper
## Overview
This is a command line tool to get statistics in a form of a table with the top 10 countries (according to the statistic chosen) along with Israel (to see how it compares with the top 10). The numbers are being updated daily and are taken from John's Hopkins University data - https://coronavirus.jhu.edu/data/mortality. 

You can use this script to setup a cronjob and get a daily report to console.

## Installation
**Note: These instructions work for UNIX-based operating systems and had been tested on MacOS with Python 3.7.3.**
1. Clone the repo to some folder
2. Open the terminal in the folder you've cloned the repo to and give execution permissions to `setup.sh` (`chmod +x setup.sh`)
3. Run `./setup.sh`. Note that you must have `/usr/local/bin` in your system `$PATH`.

## Usage
`$ covids variable [--ascending]`.  
For example, to see the top 10 countries with the highest confirmed cases (along with Israel being the 11th country with its respective rank) type: `covids confirmed`.  
For help, open the terminal and type `covids -h` to get the list of commands and usage.  

## TODO
- Make it working on Windows.
- Improve response speed when issuing only with help flag (`covids -h`)
