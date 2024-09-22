from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import requests
import re


#unit in thousand (TWD)

def find_cashflow(stock_name):
    # URL of the webpage
    url = f'https://statementdog.com/analysis/{stock_name}/cash-flow-statement'
    print(f"Accessing URL: {url}")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Path to your chromedriver (replace with the actual path)
    chromedriver_path = '/Users/jasonwang/PycharmProjects/pythonProject/Stock/chromedriver-mac-x64/chromedriver'
    print(f"Using ChromeDriver from: {chromedriver_path}")

    service = ChromeService(executable_path=chromedriver_path)

    try:
        # Start the browser
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("ChromeDriver started successfully.")

        # Set page load timeout
        driver.set_page_load_timeout(30)

        driver.get(url)
        print("Page loaded successfully.")

        # Allow time for JavaScript to render
        time.sleep(10)  # Increase wait time to ensure full rendering
        print("Waiting for JavaScript to render...")

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print("Page source parsed successfully.")

        # Find all rows in the table
        rows = soup.find_all('tr')

        # Initialize the variable to store the rightmost element
        # Initialize the variable to store the desired elements
        rightmost_element_array = []

        # Loop through each row to find the one containing '自由現金流'
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                if '自由現金流' in cell.get_text():
                    # Get the 4 rightmost elements in the row
                    rightmost_element_array = [cells[-i].get_text().strip() for i in range(1, 5)]
                    break
            if rightmost_element_array:
                break

        if rightmost_element_array:
            print(f"The 4 rightmost elements in the '自由現金流' row are: {rightmost_element_array}")

            for i in range(len(rightmost_element_array)):
                rightmost_element_array[i] = float(rightmost_element_array[i].replace(",", "")) * 1000

            return sum(rightmost_element_array)
        else:
            print("The row containing '自由現金流' was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

def find_cash_and_short_term_invest(stock_name):
    # URL of the webpage
    url = f'https://statementdog.com/analysis/{stock_name}/assets'
    print(f"Accessing URL: {url}")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Path to your chromedriver (replace with the actual path)
    chromedriver_path = '/Users/jasonwang/PycharmProjects/pythonProject/Stock/chromedriver-mac-x64/chromedriver'
    print(f"Using ChromeDriver from: {chromedriver_path}")

    service = ChromeService(executable_path=chromedriver_path)

    try:
        # Start the browser
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("ChromeDriver started successfully.")

        # Set page load timeout
        driver.set_page_load_timeout(30)

        driver.get(url)
        print("Page loaded successfully.")

        # Allow time for JavaScript to render
        time.sleep(10)  # Increase wait time to ensure full rendering
        print("Waiting for JavaScript to render...")

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print("Page source parsed successfully.")

        # Find all rows in the table
        rows = soup.find_all('tr')

        # Initialize the variables to store the desired elements
        cash_rightmost_elements = []
        short_invest_rightmost_elements = []

        # Loop through each row to find the one containing '現金及約當現金'
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                if '現金及約當現金' in cell.get_text():
                    # Get the 4 rightmost elements in the row
                    cash_rightmost_elements = [cells[-i].get_text().strip() for i in range(1, 5)]
                    break
            if cash_rightmost_elements:
                break

        # Loop through each row to find the one containing '短期投資'
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                if '短期投資' in cell.get_text():
                    # Get the 4 rightmost elements in the row
                    short_invest_rightmost_elements = [cells[-i].get_text().strip() for i in range(1, 5)]
                    break
            if short_invest_rightmost_elements:
                break

        if cash_rightmost_elements and short_invest_rightmost_elements:
            print(f"The 4 rightmost elements in the '現金及約當現金' row are: {cash_rightmost_elements}")
            print(f"The 4 rightmost elements in the '短期投資' row are: {short_invest_rightmost_elements}")

            for i in range(len(cash_rightmost_elements)):
                cash_rightmost_elements[i] = float(cash_rightmost_elements[i].replace(",", ""))

            for i in range(len(short_invest_rightmost_elements)):
                short_invest_rightmost_elements[i] = float(short_invest_rightmost_elements[i].replace(",", ""))

            return sum(cash_rightmost_elements) + sum(short_invest_rightmost_elements)

        else:
            print("The row containing '現金及約當現金' or '短期投資' wasn't found.")

    except Exception as e:
        print(f"An error occurred: {e}")

def find_total_liability(stock_name):
    # URL of the webpage
    url = f'https://statementdog.com/analysis/{stock_name}/liabilities-and-equity'
    print(f"Accessing URL: {url}")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Path to your chromedriver (replace with the actual path)
    chromedriver_path = '/Users/jasonwang/PycharmProjects/pythonProject/Stock/chromedriver-mac-x64/chromedriver'
    print(f"Using ChromeDriver from: {chromedriver_path}")

    service = ChromeService(executable_path=chromedriver_path)

    try:
        # Start the browser
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("ChromeDriver started successfully.")

        # Set page load timeout
        driver.set_page_load_timeout(30)

        driver.get(url)
        print("Page loaded successfully.")

        # Allow time for JavaScript to render
        time.sleep(10)  # Increase wait time to ensure full rendering
        print("Waiting for JavaScript to render...")

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print("Page source parsed successfully.")

        # Find all rows in the table
        rows = soup.find_all('tr')

        # Initialize the variable to store the desired elements
        rightmost_element_array = []

        # Loop through each row to find the one containing '總負債'
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                if '總負債' in cell.get_text():
                    # Get the 4 rightmost elements in the row
                    rightmost_element_array = [cells[-i].get_text().strip() for i in range(1, 5)]
                    break
            if rightmost_element_array:
                break

        if rightmost_element_array:
            print(f"The 4 rightmost elements in the '總負債' row are: {rightmost_element_array}")

            for i in range(len(rightmost_element_array)):
                rightmost_element_array[i] = float(rightmost_element_array[i].replace(",", ""))

            return sum(rightmost_element_array)

        else:
            print("The row containing '總負債' was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

def find_share_outstanding(stock_name):
    # URL of the webpage
    url = f'https://www.stockdog.com.tw/stockdog/index.php?m=overview&sid={stock_name}'
    print(f"Accessing URL: {url}")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Path to your chromedriver (replace with the actual path)
    chromedriver_path = '/Users/jasonwang/PycharmProjects/pythonProject/Stock/chromedriver-mac-x64/chromedriver'
    print(f"Using ChromeDriver from: {chromedriver_path}")

    service = ChromeService(executable_path=chromedriver_path)

    try:
        # Start the browser
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("ChromeDriver started successfully.")

        # Set page load timeout
        driver.set_page_load_timeout(120)  # Increased to 120 seconds

        driver.get(url)
        print("Page loaded successfully.")

        # Wait for specific element to be present
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'row-fluid')))
        print("Page elements loaded successfully.")

        # Allow time for JavaScript to render
        time.sleep(10)  # Explicit sleep to ensure full rendering
        print("Waiting for JavaScript to render...")

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print("Page source parsed successfully.")

        # Find the div with class 'row-fluid'
        row_fluid_divs = soup.find_all('div', class_='row-fluid')

        # Initialize the variable to store the desired number
        exterior_circulating_stock = None

        # Loop through each 'div' to find the 'h3' containing '在外流通張數'
        for div in row_fluid_divs:
            h3_tags = div.find_all('h3')
            for tag in h3_tags:
                text = tag.get_text(strip=True)  # Using strip=True to remove extra whitespace
                if '在外流通張數' in text:
                    # Extract the number using regular expression
                    match = re.search(r'在外流通張數[:：\s]*([\d,]+)張', text)
                    if match:
                        # Remove commas from the number and convert it to an integer
                        exterior_circulating_stock = int(match.group(1).replace(',', ''))
                    break
            if exterior_circulating_stock is not None:
                break

        if exterior_circulating_stock is not None:
            print(f"The '在外流通張數' value is: {exterior_circulating_stock} k張")
            return exterior_circulating_stock
        else:
            print("The '在外流通張數' data was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def calculate_cashflows(start_year, end_year, initial_cashflow, growth_rate1, growth_rate2):
    def helper(year, initial_cashflow, growth_rate1, growth_rate2):
        if year == 1:
            return initial_cashflow
        elif year >= 2 and year <= 6:
            return helper(year - 1, initial_cashflow, growth_rate1, growth_rate2) * (1+growth_rate1)
        elif year >= 7 and year <= 11:
            return helper(year - 1, initial_cashflow, growth_rate1, growth_rate2) * (1+growth_rate2)

    cashflows = []
    for year in range(start_year + 1, end_year + 1):
        cashflow = helper(year, initial_cashflow, growth_rate1, growth_rate2)
        cashflows.append(cashflow)
    return cashflows

def fair_price(stock_name):

    TTM_cashflow_annual = find_cashflow(stock_name)

    cashflow_array = calculate_cashflows(1, 11, TTM_cashflow_annual, growth_rate_within5yrs, growth_rate_2nd_5yrs)

    print(cashflow_array)

    Enterprise_value = 0
    terminal_value = cashflow_array[-1] # last one
    terminal_value *= ((1 + growth_rate_forever)/(expected_discount_rate-growth_rate_forever))
    print('terminal value is ', terminal_value)

    for i in range(len(cashflow_array)):
        Enterprise_value += cashflow_array[i] / (1 + expected_discount_rate) ** (i+1)

    print('enterprise value before adding terminal value is ', Enterprise_value)
    Enterprise_value += (terminal_value / (1 + expected_discount_rate) ** 10)

    Fair_price = Enterprise_value + (find_cash_and_short_term_invest(stock_name) * 1000)
    Fair_price -= (find_total_liability(stock_name) * 1000)
    Fair_price /= (find_share_outstanding(stock_name) * 1000)
    return Fair_price

stock_name = input("Enter the stock code: ")
growth_rate_within5yrs = float(input("Enter the growth rate within 5 yrs(in decimal): "))
growth_rate_2nd_5yrs = float(input("Enter the growth rate for the 2nd 5 yrs(in decimal): "))
growth_rate_forever = float(input("Enger the forever growth rate after 10 years(in decimal): "))
expected_discount_rate = float(input("Enter your expected discounted rate(in decimal): "))

print(fair_price(stock_name))


# find_cashflow(stock_name)
# find_cash_and_short_term_invest(stock_name)
# find_total_liability(stock_name)
# find_share_outstanding(stock_name)
# find_growth_rate_within5yrs()
