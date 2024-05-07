from data_parser import *

ticker = "TSLA" #input("Enter the ticker: ").strip().upper()

response, y = generate_insights(ticker, "fast")
print(response.text)

## First download the data
