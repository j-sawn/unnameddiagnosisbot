import requests
from bs4 import BeautifulSoup

#TO-DO
# No consideration of HTML decor (e.g. bolded letters, links)
# Also no consideration for different formats (e.g. "Scabies Symptoms" instead of "Symptoms of Scabies") or synonyms (e.g. "Signs of Bowen's Disease" instead of "Symptoms of Bowen's Disease")
# kind of shoddy ngl

conditions = ["boils", "cellulitis", "chilblains", "frostbite", "impetigo-school-sores", "leg-ulcers", "pityriasis-rosea", 
              "melanoma", 
              "eczema-atopic-dermatitis", "mccune-albright-syndrome", "psoriasis", "sunburn",
              "bedbugs", "body-lice", "fleas", "hives"]
all_symptoms = []

for condition in conditions:

    # Making a GET request
    url = 'https://www.betterhealth.vic.gov.au/health/conditionsandtreatments/' + condition
    r = requests.get(url)

    # parse content
    soup = BeautifulSoup(r.content, 'html.parser')

    # get main section of article
    div = soup.find('div', {"class":"bhc-content__components"}) #Finds the div with class "_1lwNBHmCQJObvqs1fXKSYR"


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

    # turn into list of symptoms and then add it to the universal list of all symptoms
    symptoms = excerpt.split("<li>")
    symptoms.remove('') # fix
    symptoms.remove('') # fix
    all_symptoms.append(symptoms)

# TESTING FUNCTION: Prints all symptoms collected by the above program (UNCOMMENT TO USE)
#for symptom in all_symptoms:
#    print(symptom)