# FinTech_Lab_summerTask
Programming Task for Fintech Lab

### Downloads
User needs to install following dependencies to run the program locally (we use python):

pip install -U sec-edgar-downloader
pip install -q -U google-generativeai
pip install flask
pip install markdown2

The first install is for the sec edgar data API
The second install is for the inference prompt for the LLM
The third and fourth install are for the app (which I currently run locally)

### The python files
data_parser.py contains all functions needed seperately. I used human readable primary-document.html insteead of full-submission.txt because I could parse the former one better and the latter contained (in my opinion) data that was unnecessary. This seperation is to resolve any errors that might occur within individual functions. I use the gemini-pro as it is a good chatbot that I have previously used.

I parse the data by choosing only specific sections of the document and feeding them to the LLM. After this, the task was a prompt engineering question and in the end, I first summarized the data for each year and then used those summaries to generate a final summary of the progress of the company. I could probably do better but this was the best option I reached. This was because the initial file was too long and I could not input the whole thing to the LLM itself.


main_functionality.py can be used to test the function without using the app.

app.py contains the app functionality that displays the generated output from the LLM. Put in any ticker and then the speed at which you wish to process and you will get the output.


### Tech Stack
I used python because I am proficient in the language and it is very simple to make API calls usin python. I used Flask for the app because that was the simplest app coding I could find (I am not very familiar with making apps/websites).

### Outputs
A few outputs have been stored in Tesla_output.txt and Doordash_output.txt

### Link to the recording : 

P.S. : I used the late days because I had a 24 hr journey back home and I had to move out of my apartment. Sorry for the delay!! I hope I can be accepted into the lab.

