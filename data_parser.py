from sec_edgar_downloader import Downloader
import os
import re
from bs4 import BeautifulSoup
import textwrap

import google.generativeai as genai

# from IPython.display import display
from IPython.display import Markdown

# path = "./download_files/sec-edgar-filings/"

def download_data(ticker, path = "./download_files"):
    """
    Function to download the data from the SEC site in human readable format (which will be present in primary-document.html)
    Args:
        ticker (str) : The name of the company filings to download
        path (str) : the path where this data is downloaded
    Return:
        (bool) : if the download worked or not. False generally means that the company does not exist.
    """
    dl = Downloader("GTARC", "agupta886@gatech.edu", path)
    try:
        dl.get("10-K", ticker, download_details = True)
        return True
    except:
        return False

## We save the downloaded data to ./download_files/sec-edgar-filings/<ticker>
## Test downloads
# download_data("TSLA", "./download_files")
# download_data("AAPL", "./download_files")


def return_dataparsed(path):
    """
    Function that returns human readable data by parsing through the human readbale HTML provided by the downloader
    Args:
        path (str) : The path of the .html file to parse through
    Return:
        parsed_data (str) : The html file converted to text that can be fed into the LLM
    """
    file = open(path, "r")
    data = file.read()
    file.close()
    parsed_data = BeautifulSoup(data, features="html.parser")
    
    ret_data = ' '.join(parsed_data.get_text().split())
    return re.sub(r'[^\x00-\x7F]+', '', ret_data)

##Example usage
# print(return_dataparsed("full-submission.txt"))

def read_files_in_subdirectory(ticker, directory = "./download_files/sec-edgar-filings/"):
    """
    Function to read all the human-readable HTML files to create input data for the LLM model.
    Args:
        ticker (str) : The name of the company filings to download
        directory (str) : The source directory where the filings for this ticker will be found
    """
    directory += ticker + "/"
    file_paths = []
    # Iterate over all files and subdirectories in the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has a .txt extension
            if file.endswith(".html"):
                # Construct the full path to the file
                file_path = os.path.join(root, file)
                # Read the contents of the file and append it to the list
                file_paths.append(file_path)
    return file_paths

## Example usage
# file_paths = read_files_in_subdirectory("MSFT")
# for i in file_paths:
#     print(i)

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def llm_prompt(file_paths, ticker):
    """
    Given an input, this function passes the input to the llm and generates a response. We use gemini-pro for the response.
    text: the input to be sent to the LLM
    """

    GOOGLE_API_KEY = 'AIzaSyAIgAYQMG6oovlHJD3F-1RsLFEJJBTYI30'
    genai.configure(api_key=GOOGLE_API_KEY)
    # for m in genai.list_models():
    #   if 'generateContent' in m.supported_generation_methods:
    #     print(m.name)

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    text1 = f"The following are 10-K filing summaries of each year of {ticker}. Summarize the growth of the company and some insights:"
    text = f"The following is data from {ticker} 10-k filings, summarize them in a few paragraphs and provide some interesting insights about the company :"
    # for file_path in file_paths:
    #     response = model.generate_content(text + return_dataparsed(file_path))
    #     text1 += "\n" + response.text
    inp_txt = text + return_dataparsed(file_paths[0])
    response = model.generate_content(inp_txt)
    text1 += "\n" + response.text
    print("llm response generating.....")
    response = model.generate_content(text1)
    
    return response

def generate_insights(ticker):
    """
    given a ticker for a company, generate a response from the information extracted from the filings
    """
    path = "./download_files/sec-edgar-filings/" + ticker
    
    downloaded = download_data(ticker)

    ## Check if successful
    if not downloaded:
        raise ValueError("The ticker input is incorrect. Please try correct ticker.")
    else:
        print("10-K data downloaded, continuing to processing.....")

    file_paths = read_files_in_subdirectory(ticker)
    
    print(f"{len(file_paths)} year(s) of data being processed.....")

    ## llm functionality
    response = llm_prompt(file_paths, ticker)
    
    os.rmdir(path)

    return response