# FinTech_Lab_summerTask
Programming Task for Fintech Lab
User needs to install following dependencies to run the program locally:

pip install -U sec-edgar-downloader
python -m pip install mediapipe

The first install is for the sec edgar data API
The second install is for the inference prompt for the LLM

data_parser.py downloads and cleans the data. I used human readable primary-document.html insteead of full-submission.txt because I could parse the former one better and the latter contained (in my opinion) data that was unnecessary.

main_functionality.py uses this data and gives it to the LLM. I use the Gemma-2b model as it was described as a reasoning model with good summarization abilities. The main problem was what one would consider as an insight. This was a prompt engineering question and in the end, I used the prompt "" to get insights about the data. I could probably do better but this was the best option I reached.


