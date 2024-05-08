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


def return_dataparsed(path, option):
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
    
    # ret_data = ' '.join(parsed_data.get_text().split())
    if option == "slow":
        ret_data = parsed_data.get_text()
        ret_data = re.sub(r'[^\x00-\x7F]+', '', ret_data)
        ret_data = " ".join(ret_data.split()).lower()
        idx_pt1 = ret_data.index("ITEM 1. BUSINESS".lower())
        ret_data = ret_data[idx_pt1 :]
        idx_pt1 = ret_data.index("ITEM 1. BUSINESS".lower())
        idx_pt2 = ret_data.index("PART II".lower())
        idx_pt3 = ret_data.index("PART III".lower())
        part2_data = ret_data[idx_pt2 : idx_pt3]
        return part2_data
    else:
        ret_data = parsed_data.get_text()
        ret_data = re.sub(r'[^\x00-\x7F]+', '', ret_data)
        ret_data = " ".join(ret_data.split()).lower()
        idx_pt1 = ret_data.index("ITEM 1. BUSINESS".lower())
        ret_data = ret_data[idx_pt1 :]
        idx_pt1 = ret_data.index("ITEM 1. BUSINESS".lower())
        idx_pt2 = ret_data.index("Financial statements and Supplementary Data".lower())

        idx_pt3 = ret_data.index("PART III".lower())
        part2_data = ret_data[idx_pt2 : idx_pt3]
        return part2_data


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

def send_parts(model, part):
    k = 10000
    split = part.split()
    summary = ""
    for i in range(len(split)//k):
        s = " ".join(split[i * k : (i+1)*k])
        try:
            r = model.generate_content("Summarize the following in a few paragraphs:\n" + s)
            summary += r.text
        except:
            continue
    return summary

def llm_prompt(file_paths, ticker, option):
    """
    Given an input, this function passes the input to the llm and generates a response. We use gemini-pro for the response.
    text: the input to be sent to the LLM
    """

    GOOGLE_API_KEY = 'AIzaSyA8Gt8GITRmfHdp_HGswt5Z4amWbDob_Ko'
    genai.configure(api_key=GOOGLE_API_KEY)

    y = 0
    model = genai.GenerativeModel('gemini-pro')
    text1 = f"The following are 10-K filing summaries of each year of {ticker}. Summarize the growth of the company and provide some insights:\n"
    final_text = ""
    for file_path in file_paths:
        try:
            part1 = return_dataparsed(file_path, option)
            response = send_parts(model, part1)
        except:
            pass
        
        while True:
            try:
                response = model.generate_content(f"Summarize these summaries of the 10-k filings of {ticker} in a few paragraphs:\n" + response).text
                break
            except:
                pass
        y += 1
        print(y)
        final_text += response
    
    # inp_txt = return_dataparsed(file_paths[0])
    # response = chat.send_message(inp_txt)
    final_text = text1 + final_text
    print("llm response generating.....")
    while True:
        try:
            response = model.generate_content(text1)
            break
        except:
            pass
    return response

def generate_insights(ticker, option = 'fast'):
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
    response = llm_prompt(file_paths, ticker, option)

    return response