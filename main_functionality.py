from data_parser import *

ticker = "DASH" #input("Enter the ticker: ").strip().upper()

response = generate_insights(ticker, "slow")
print(response.text)

## First download the data
