import CYKParse
import Tree
import requests
from datetime import date


#default Temperature type value (global variable)
today = date.today()
d1 = today.strftime("%Y-%m-%d")
currentyear = str(int(date.today().strftime("%Y-%m-%d")[0:4]) - 10)
dateyearago = currentyear + d1[4:]
def K2F(K):
    return (K - 273.15) * 1.8 + 32

def K2C(K):
    return (K - 273.15)

def F2K(F):
    return (F - 32) * 0.5555 + 273.15

def F2C(F):
    return (F - 32) * 0.5555


cityList = [(5359777, "Irvine"),(5379513, "Orange"),(5323810, "Anaheim"),
(5376890, "Newport Beach"), (5323163, "Aliso Viejo"),(5330582, "Brea"),
(5331575, "Buena Park"), (5339840, "Costa Mesa"), (5341256, "Cypress"),
(5341483,"Dana Point"), (5350207, "Fountain Valley"), (5351247, "Fullerton"),
(5351515, "Garden Grove"), (5358705, "Huntington Beach"), (5363922, "La Habra"),
(5364022, "La Palma"),(5364275, "Laguna Beach"), (5364306, "Laguna Hills"),
(5364329, "Laguna Niguel"), (5364369, "Laguna Woods"), (5364514 ,"Lake Forest"),
(5368304, "Los Alamitos"), (5373763, "Mission Viejo"), (5383527, "Placentia"),
(5386082, "Rancho Santa Margarita"), (5391791, "San Clemente"),
(5392229, "San Juan Capistrano"), (5392900, "Santa Ana"), (5394086, "Seal Beach"),
(5398630, "Stanton"), (5404119, "Tustin"), (5406337, "Villa Park"),
(5408406, "Westminister"), (5410902, "Yorba Linda")]



#empty dictionary
dict = {}
dict_h = {}
#iterates through list using ids
for id in cityList:
    #url for the API
    url = "http://api.openweathermap.org/data/2.5/weather?id={0}&appid=9f3e3db5e1c0af3fd17ac4b853de94ea".format(id[0])
    #gets responses from the url call using requests
    response = requests.get(url)
    #stores data into empty dictionary based off of the corresponding ids for
    #each city
    dict[id[1]] = response.json()
    # print("CURRENT CITY - {0} - KELVIN".format(id[1]), dict[id[1]]['main']['temp'])
    # print("CURRENT CITY - {0} - CENTGRADE".format(id[1]), K2C(dict[id[1]]['main']['temp']))
    # print("CURRENT CITY - {0} - FARENHEIT".format(id[1]), K2F(dict[id[1]]['main']['temp']))
# print(dict['Irvine']['list'][0]['main'])
# print("DICTIONARY", dict['Irvine']['main']['temp'])


for id in cityList:
    cityname = id[1]
    url2 = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={0}, CA&num_of_days=1&date={1}&key=d7d7d81e4cd44b73b7f225527211503&format=json".format(cityname,dateyearago)
    response2 = requests.get(url2)
    dict_h[cityname] = response2.json()['data']['weather'][0]['avgtempF']

def get_temp(city):
    if TEMP == 'K':
        return str(dict[city]['main']['temp'])
    if TEMP == 'C':
        return str(K2C(dict[city]['main']['temp']))
    if TEMP == 'F':
        return str(K2F(dict[city]['main']['temp']))

def get_historicaltemp(city):
    if TEMP == 'K':
        return str(F2K(int(dict_h[city])))
    if TEMP == 'C':
        return str(F2C(int(dict_h[city])))
    if TEMP == 'F':
        return str(dict_h[city])

def difference(city):

    value = (float(get_temp(city)) - float(get_historicaltemp(city)))
    return abs(value)

requestInfo = {
        'name': '',
        'time': '',
        'location': '',
        'type' : '',
        'secondTime': ''
        }
haveGreeted = False



# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0')}
    completeSentenceTree = max(sentenceTrees.keys())
    #print('getSentenceParse', completeSentenceTree)
    return T[completeSentenceTree]

# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo
    lookingForLocation = False
    lookingForName = False

    requestInfo['time'] = ''
    requestInfo['location'] = ''

    for leaf in Tr.getLeaves():
        #print("LEAF: ", leaf)
        if leaf[0] == 'Preposition' and leaf[1] == 'than':
            requestInfo['type'] = 'compare'
        if leaf[0] == 'Adverb':
            if requestInfo['time'] != '':
                requestInfo['secondTime'] = leaf[1]
            else:
                requestInfo['time'] = leaf[1]

        if lookingForLocation and leaf[0] == 'Name':
            requestInfo['location'] = leaf[1]
        if leaf[0] == 'Preposition' and leaf[1] == 'in':
            lookingForLocation = True
        else:
            lookingForLocation = False
        if leaf[0] == 'Noun' and leaf[1] == 'name':
            lookingForName = True
        if lookingForName and leaf[0] == 'Name':
            requestInfo['name'] = leaf[1]

# This function contains the data known by our simple chatbot
# def getTemperature(location, time):
#     return str(K2F(dict[location]['main']['temp']))

# Format a reply to the user, based on what the user wrote.
def reply():
    global requestInfo
    global haveGreeted

    if requestInfo['location'] == '':
        print("Please provide a defined location!\n")
        return False

    elif requestInfo['type'] == 'compare':
        print("REQUEST", requestInfo)
        if int(get_temp(requestInfo['location'], requestInfo['time'])) > int(get_temp(requestInfo['location'], requestInfo['secondTime'])):
            print('Yes, in ' + requestInfo['location'] + ', ' +  requestInfo['time']  + ' is hotter than ' + requestInfo['secondTime'] + '.')
            return True
        else:
            print('No, in ' + requestInfo['location'] + ', ' +  requestInfo['time']  + ' is not going to be hotter than ' + requestInfo['secondTime']+ '.')
            return True
        #compare temps HERE
    else:
        if not haveGreeted and requestInfo['name'] != '':
            print("Hello", requestInfo['name'] + '.')
            haveGreeted = True
            return True

        time = 'now' # the default
        if requestInfo['time'] != '':
            time = requestInfo['time']
        salutation = ''

        if requestInfo['time'] == 'now' or requestInfo['time'] == 'today':
            # salutation = requestInfo['name'] + ', '
            print(salutation + '\nThe temperature in ' + requestInfo['location'] + ' ' +
                time + ' is ' + get_temp(requestInfo['location']) + ' degrees.')
            return True

        elif requestInfo['time'] == 'ten':
            # salutation = requestInfo['name'] + ', '
            print(salutation + '\nThe temperature in ' + requestInfo['location'] + ' ' +
                time + ' years ago was ' + get_historicaltemp(requestInfo['location']) + ' degrees.')
            return True

        elif requestInfo['time'] == 'changed':
            print ('\nThe temperature has changed by ' + str(difference(requestInfo['location'])) + ' degrees over the past ten years.')
            return True

        else:
            print ('Incorrect sentence structure, please try again.\n')
            return False

# A simple hard-coded proof of concept.
def main():
    global requestInfo
    print("\nHi, welcome to the weather chatbot!")
    print("Would you like your weather reports to be in Fahrenheit, Celsius, or Kelvin?\n")
    input1 = input()
    while (input1 != "Fahrenheit" and input1 != "Celsius" and input1 != "Kelvin"):
        print("Error, please type Fahrenheit, Celsius, or Kelvin.\n")
        input1 = input()

    #print("INPUT1", input1)
    print("\nOkay perfect, the temperatures will be listed according to what you picked")
    print("How can I help you today?\n")
    input2 = input().split(" ")
    global TEMP
    TEMP = 'K'
    if(input1 == "Fahrenheit"):
        TEMP = 'F'
    if(input1 == "Celsius"):
        TEMP = 'C'

    T, P = CYKParse.CYKParse(input2, CYKParse.getGrammarWeather())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    response = reply()
    while (response == False):
        input2 = input().split(" ")
        T, P = CYKParse.CYKParse(input2, CYKParse.getGrammarWeather())
        sentenceTree = getSentenceParse(T)
        updateRequestInfo(sentenceTree)
        response = reply()


    print("Anything else I can help you with? \n")

    response = False
    while (response == False):
        input3 = input().split(" ")
        T, P = CYKParse.CYKParse(input3, CYKParse.getGrammarWeather())
        sentenceTree = getSentenceParse(T)
        updateRequestInfo(sentenceTree)
        response = reply()



    print("Anything else I can help you with? \n")

    response = False
    while (response == False):
        input4 = input().split(" ")
        T, P = CYKParse.CYKParse(input4, CYKParse.getGrammarWeather())
        sentenceTree = getSentenceParse(T)
        updateRequestInfo(sentenceTree)
        reply()


main()
