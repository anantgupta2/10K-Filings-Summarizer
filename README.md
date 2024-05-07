# FinTech_Lab_summerTask
Programming Task for Fintech Lab

### Downloads
User needs to install following dependencies to run the program locally (we use python):

pip install -U sec-edgar-downloader
pip install -q -U google-generativeai

The first install is for the sec edgar data API
The second install is for the inference prompt for the LLM

### The python files
data_parser.py contains all functions needed seperately. I used human readable primary-document.html insteead of full-submission.txt because I could parse the former one better and the latter contained (in my opinion) data that was unnecessary. This seperation is to resolve any errors that might occur within individual functions. I use the gemini-pro as it is a good chatbot that I have previously used.

I parse the data by choosing only specific sections of the document and feeding them to the LLM. After this, the task was a prompt engineering question and in the end, I first summarized the data for each year and then used those summaries to generate a final summary of the progress of the company. I could probably do better but this was the best option I reached.


main_functionality.py just combines all the functions to produce an interpretable output.

app.py contains the app functionality that uses the final function in main_functionality.py


### Tech Stack
I used python because I am proficient in the language and it is very simple to make API calls usin python. I used Flask for the app because that was the simplest app coding I could find (I am not very familiar with making apps/websites).

### Link to the recording : 

P.S. : I used the late days because I had a 24 hr journey back home and I had to move out of my apartment. Sorry for the delay.

