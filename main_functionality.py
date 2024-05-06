from data_parser import *
import mediapipe as mp
from mediapipe.tasks.python import text

ticker = input("Enter the ticker: ").strip().upper()

response = generate_insights(ticker)
print(response.text)

## First download the data
