import requests
from bs4 import BeautifulSoup

# unit in million (USD)

def find_cashflow(stock_name):
    # URL of the webpage
    url = f'https://stockanalysis.com/stocks/{stock_name}/financials/cash-flow-statement/'

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the data
        table = soup.find('table', {'id': 'main-table'})

        # Find the row that contains "Revenue"
        free_cashflow_row = None
        for row in table.find_all('tr'):
            if 'Free Cash Flow' in row.text:
                free_cashflow_row = row
                break

        if free_cashflow_row:
            # Extract the cell in the "TTM" column
            ttm_cell = free_cashflow_row.find_all('td')[1]  # Assuming TTM is the second cell
            ttm_value = ttm_cell.text.strip()
            print(f'The extracted TTM Free cashflow value is: {ttm_value}')
            return float(ttm_value.replace(",", ""))
        else:
            print('Free Cashflow row not found')
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

def find_cash_and_short_term_invest(stock_name):
    # URL of the webpage
    url = f'https://stockanalysis.com/stocks/{stock_name}/financials/balance-sheet/'

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the data
        table = soup.find('table', {'id': 'main-table'})

        # Find the row that contains "Revenue"
        free_cash_and_short_term_invest_row = None
        for row in table.find_all('tr'):
            if 'Cash & Short-Term Investments' in row.text:
                free_cash_and_short_term_invest_row = row
                break

        if free_cash_and_short_term_invest_row:
            # Extract the cell in the "TTM" column
            ttm_cell = free_cash_and_short_term_invest_row.find_all('td')[1]  # Assuming TTM is the second cell
            ttm_value = ttm_cell.text.strip()
            print(f'The extracted TTM Cash & Short-Term Investments value is: {ttm_value}')
            return float(ttm_value.replace(",", ""))
        else:
            print('Cash & Short-Term Investments row not found')
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

def find_total_debt(stock_name):
    # URL of the webpage
    url = f'https://stockanalysis.com/stocks/{stock_name}/financials/balance-sheet/'

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the data
        table = soup.find('table', {'id': 'main-table'})

        # Find the row that contains "Revenue"
        total_debt_row = None
        for row in table.find_all('tr'):
            if 'Total Debt' in row.text:
                total_debt_row = row
                break

        if total_debt_row:
            # Extract the cell in the "TTM" column
            ttm_cell = total_debt_row.find_all('td')[1]  # Assuming TTM is the second cell
            ttm_value = ttm_cell.text.strip()
            print(f'The extracted TTM Total liabilities value is: {ttm_value}')
            return float(ttm_value.replace(",", ""))
        else:
            print('Total liabilities row not found')
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

def find_share_outstanding(stock_name):
    # URL of the webpage
    url = f'https://stockanalysis.com/stocks/{stock_name}/'

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific table using its class
        table = soup.find('table',
                          class_='w-[48%] text-sm text-gray-900 dark:text-dark-200 tiny:text-small lg:w-auto lg:min-w-[210px]')

        shares_out_value = None

        # Check if the table is found
        if table:
            # Find the row containing "Shares Out"
            for row in table.find_all('tr'):
                if 'Shares Out' in row.text:
                    # Extract the value cell
                    value_cell = row.find_all('td')[1]  # The second td should contain the value
                    shares_out_value = value_cell.text.strip()
                    break

        if shares_out_value:
            print(f'The extracted Shares Out value is: {shares_out_value}')

            if "B" in shares_out_value:
                # Remove the 'B' and convert to integer, then multiply by 1,000
                cleaned_value = shares_out_value.replace("B", "")
                final_value = float(cleaned_value) * 1000
            elif "M" in shares_out_value:
                # Remove the 'M' and convert to integer
                cleaned_value = shares_out_value.replace("M", "")
                final_value = float(cleaned_value)
            else:
                # Just convert to integer
                final_value = float(shares_out_value)

            return final_value

        else:
            print('Shares Out value not found in the table.')
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

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
    TTM_cashflow = find_cashflow(stock_name)

    cashflow_array = calculate_cashflows(1, 11, TTM_cashflow, growth_rate_within5yrs, growth_rate_2nd_5yrs)

    print(cashflow_array)

    Enterprise_value = 0
    terminal_value = cashflow_array[-1] # last one
    terminal_value *= ((1 + growth_rate_forever)/(expected_discount_rate-growth_rate_forever))
    print('terminal value is ', terminal_value)

    for i in range(len(cashflow_array)):
        Enterprise_value += cashflow_array[i] / (1 + expected_discount_rate) ** (i+1)

    print('enterprise value before adding terminal value is ', Enterprise_value)
    Enterprise_value += (terminal_value / (1 + expected_discount_rate) ** 10)

    Fair_price = Enterprise_value + find_cash_and_short_term_invest(stock_name)
    Fair_price -= find_total_debt(stock_name)
    Fair_price /= find_share_outstanding(stock_name)

    return Fair_price


stock_name = input("Enter the stock code: ")
growth_rate_within5yrs = float(input("Enter the growth rate within 5 yrs(in decimal): "))
growth_rate_2nd_5yrs = float(input("Enter the growth rate for the 2nd 5 yrs(in decimal): "))
growth_rate_forever = float(input("Enter the forever growth rate after 10 years(in decimal): "))
expected_discount_rate = float(input("Enter your expected discounted rate(in decimal): "))

print(fair_price(stock_name))

# find_cashflow(stock_name)
# find_cash_and_short_term_invest()
# find_total_debt()
# find_share_outstanding()
# find_growth_rate_within5yrs()
