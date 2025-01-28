import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

#TO-DO
# No consideration for different formats (e.g. "Scabies Symptoms" instead of "Symptoms of Scabies" OR paragraphs used instead of lists) or synonyms (e.g. "Signs of Bowen's Disease" instead of "Symptoms of Bowen's Disease")
# kind of shoddy ngl

conditions = [
              # ones that work well on their own
              "boils", "cellulitis", "chilblains", "frostbite", "impetigo-school-sores", "leg-ulcers", "pityriasis-rosea", 
              "melanoma", 
              "eczema-atopic-dermatitis", "mccune-albright-syndrome", "psoriasis", 
              "sunburn",
              "bedbugs", "body-lice", "fleas", "hives",
              
              # ones that had to have measures taken in place (indicates inefficiency)
              "blisters", "cold-sores", "tinea", "warts",
              "blushing-and-flushing", 
              "erythema-nodosum", "leprosy", "rosacea", "scleroderma"]
all_symptoms = []

for condition in conditions:

    # Making a GET request
    url = 'https://www.betterhealth.vic.gov.au/health/conditionsandtreatments/' + condition
    r = requests.get(url)

    # parse content
    soup = BeautifulSoup(r.content, 'html.parser')

    # get main section of article
    div = soup.find('div', {"class":"bhc-content__components"})


    # find list of symptoms, extract each dot point, and then compile it all in a list of symptoms in the same position as its respective disease 

    # TO-DO: SIMPLIFY!!!

    # find symptoms section of article
    excerpt = str(div)
    start = excerpt.find('<h2 id="symptoms')
    excerpt = excerpt[start:]
    end = excerpt.find('</ul>')
    excerpt = excerpt[:end]

    # reduce section to just the dot points
    start = excerpt.find('<li')
    excerpt = excerpt[start:]

    # turn into a workable string that can be split and put into a list
    excerpt = excerpt.replace("</li>", "<li>") # fix
    excerpt = excerpt.replace("<li> <li>", "<li>") # fix
    excerpt = excerpt.replace("<li><li>", "<li>") # fix
    excerpt = excerpt.replace("<li>", "[break]") # fix

    # in case links have html tag
    while excerpt.find('<') != -1:
        start = excerpt.find('<')
        end = excerpt.find('>')
        substring = excerpt[start:end+1]
        excerpt = excerpt.replace(substring, '')
        #print(excerpt)


    # turn into list of symptoms and then add it to the universal list of all symptoms
    symptoms = excerpt.split("[break]")
    symptoms.remove('') # fix
    symptoms.remove('') # fix
    all_symptoms.append(symptoms)

    # add a delay between requests to avoid overwhelming the website with requests (CAUSES DELAYS)
    time.sleep(1)

# TESTING FUNCTION: Prints all symptoms collected by the above program (UNCOMMENT TO USE)
#for symptom in all_symptoms:
#    print(symptom)

# OPTIONAL: converts data scraped to a workable .json file (UNCOMMENT TO USE)
#archive_dict = {
#    'condition_names' : conditions,
#    'symptom_lists' : all_symptoms
#}
#archive_df = pd.DataFrame.from_dict(archive_dict)
#archive_df.to_json('archive.json')
