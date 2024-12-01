# Web Crawler and DCF calculator for Stocks (Taiwan and US)

## Overview

This repository contains two separate web scraping scripts for extracting financial data for Taiwan stock market and US stock market. It will then run the discounted cashflow formula based on your assumption input to give you a reference fair stock price.

For Taiwan market data, source of truth: https://statementdog.com/

For US market data, source of truth: https://stockanalysis.com/

1. **`webcrawler_tw.py`**: Scrapes financial data (Cash Flow, Short-Term Investments, Total Liabilities, etc.) for Taiwanese stocks from the **Statement Dog** and **Stock Dog** websites.
2. **`webcrawler_us.py`**: Scrapes financial data (Cash Flow, Short-Term Investments, Total Liabilities, etc.) for US stocks from the **Stock Analysis** website.

Both scripts calculate the fair price of stocks by retrieving key financial metrics, and then using a discounted cash flow (DCF) model to estimate their value.

---

## Prerequisites

Before running these scripts, make sure you have the following Python packages installed:

- `selenium` for automating web browser interactions.
- `beautifulsoup4` for HTML parsing.
- `requests` for sending HTTP requests.
- `chromedriver` for automating Chrome browser (for `webcrawler_tw.py` only).

### Install Dependencies

To install the required Python packages, run the following command: pip install selenium beautifulsoup4 requests

## Running the Scripts

## `webcrawler_us.py`

This script scrapes financial data for US stocks and calculates their fair price using the DCF model.

#### Input Parameters:
- **Stock Code**: Enter the stock code (e.g., US: "AAPL" for Apple; TW: "2330" for TSMC ).
- **Growth Rates**: Enter the growth rates for the next 5 years, the 2nd 5 years, and the forever growth rate (all as decimals, e.g., 0.05 for 5%).
- **Expected Discount Rate**: Enter the expected discounted rate (e.g., 0.10 for 10%).

#### Example Input:
```text
Enter the stock code: AAPL
Enter the growth rate within 5 yrs (in decimal): 0.06
Enter the growth rate for the 2nd 5 yrs (in decimal): 0.05
Enter the forever growth rate after 10 years (in decimal): 0.03
Enter your expected discounted rate (in decimal): 0.08
