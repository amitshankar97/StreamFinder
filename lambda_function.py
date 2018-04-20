import requests
from justwatch import JustWatch

idToName = {
        8: "Netflix",
        15: "Hulu",
        9: "Amazon Prime Video",
        92: "Yahoo View",
        10: "Amazon Instant Video",
        27: "HBO Now",
        83: "The CW",
        3: "Google Play Movies",
        43: "Starz",
        2: "Apple iTunes",
        105: "FandangoNOW",
        7: "Vudu",
        188: "YouTube Red",
        191: "Kanopy",
        78: "CBS",
        37: "Showtime",
        123: "Fox",
        73: "Tubi TV",
        18: "PlayStation",
        68: "Microsoft Store",
        139: "Max Go", 102: "FilmStruck", 31: "HBO Go", 148: "ABC", 12: "Crackle", 162: "AMC Theatres", 80: "AMC", 25: "Fandor", 190: "Curiosity Stream", 79: "NBC", 34: "Epix", 155: "History", 156: "A&E", 157: "Lifetime", 99: "Shudder", 185: "Screambox", 87: "Acorn TV", 143: "Sundance Now", 151: "BritBox", 100: "GuideDoc", 14: "realeyz", 11: "Mubi", 60: "Fandango", 175: "Netflix Kids"
    }

shortNames = {
    "Netflix": "nfx",
    "Hulu": "hlu",
    "Amazon Prime Video": "amp",
    "Yahoo View": "vyh",
    "Amazon Instant Video": "amz",
    "HBO Now": "hbn",
    "HBO now": "hbn",
    "The CW": "tcw",
    "Google Play Movies": "ply",
    "Starz": "stz",
    "Apple iTunes": "itu",
    "FandangoNOW": "fdg",
    "Vudu": "vdu",
    "YouTube Red": "ytr",
    "Kanopy": "knp",
    "CBS": "cbs",
    "Showtime": "sho",
    "Fox": "fxn",
    "FXNow": "fxn",
    "Tubi TV": "tbv",
    "PlayStation": "pls",
    "Microsoft Store": "msf",
    "Max Go": "mxg",
    "FilmStruck": "fsk",
    "HBO Go": "hbg",
    "ABC": "abc",
    "Crackle": "crk",
    "AMC Theatres": "amt",
    "AMC": "amc",
    "Fandor": "fnd",
    "Curiosity Stream": "cts",
    "NBC": "nbc",
    "Epix": "epx",
    "History": "his",
    "A&E": "aae",
    "Lifetime": "lft",
    "Shudder": "shd",
    "Screambox": "scb",
    "Acorn TV": "act",
    "Sundance Now": "sdn",
    "BritBox": "bbo",
    "GuideDoc": "gdc",
    "realeyz": "rlz",
    "Mubi": "mbi",
    "Fandango": "fad",
    "Netflix Kids": "nfk"
}

listSupported = ["Netflix", "Hulu", "Amazon Prime Video", "HBO Now", "HBO now", "YouTube Red", "HBO Go", "Fox"]



def build_response(msg):
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': msg
            },
            'shouldEndSession': True
        }
    }

def responseWithCard(msg, title):
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': msg
            },
            'card': {
                "type": "Simple",
                "title": title,
                "content": msg,
            },
            'shouldEndSession': True
        }
    }

def handleTV(event, just_watch):
    show = event['request']['intent']['slots']['show']['value']
    print('show', show)
    results = {}

    if('value' not in event['request']['intent']['slots']['service']):
        results = just_watch.search_for_item(
                                    content_types=['show'],
                                    query=show)

        if results['total_results'] == 0:
            return responseWithCard("Sorry. " + show + " isn't available to stream.", "Error")

    else:
        service = event['request']['intent']['slots']['service']['value']
        print('service: ', service)

        if service not in listSupported:
            return responseWithCard("Sorry. " + service + " isn't supported yet.", "Error")

        results = just_watch.search_for_item(
                                        providers=[shortNames[service]],
                                        content_types=['show'],
                                        query=show)

        if results['total_results'] == 0:
            return responseWithCard("Sorry. " + show + " isn't available on " + service, "Error")

    print(results)
    providersFound = []
    msg = ""

    found = False

    for result in results['items']:
        print('show: ' + show)
        print('result title.lower(): ' + result['title'].lower())
        if result['title'].lower() == show:
            found = True
            show = result['title']

            services = result['offers']

            for service in services:
                if service['monetization_type'] == 'flatrate' or service['monetization_type'] == 'free':
                    if service['provider_id'] not in providersFound:
                        if service['provider_id'] in idToName:
                            providersFound.append(service['provider_id'])

            break

    if found == True:
        msg = "You can watch " + show + " on " + idToName[providersFound[0]]
        print(providersFound)

        for i in range(1, len(providersFound)):
            if i == len(providersFound) - 1:
                msg += " and " + idToName[providersFound[i]]
            else:
                msg += ", " + idToName[providersFound[i]]

        msg += "."

        return responseWithCard(msg, show)

    else:
        return responseWithCard("Sorry. I couldn't find any streaming services for " + show)

def handleMovies(event, just_watch):
    movie = event['request']['intent']['slots']['movie']['value']
    print('movie:', movie)
    results = {}

    if('value' not in event['request']['intent']['slots']['service']):
        results = just_watch.search_for_item(
                                    content_types=['movie'],
                                    query=movie)

        if results['total_results'] == 0:
            return responseWithCard("Sorry. " + movie + " isn't available to stream.", "Error")

    else:
        service = event['request']['intent']['slots']['service']['value']
        print('service: ', service)

        if service not in listSupported:
            return responseWithCard("Sorry. " + service + " isn't supported yet.", "Error")

        results = just_watch.search_for_item(
                                        providers=[shortNames[service]],
                                        content_types=['movie'],
                                        query=movie)

        if results['total_results'] == 0:
            return responseWithCard("Sorry. " + movie + " isn't available on " + service, "Error")

    print(results)

    providersFound = []
    msg = ""

    found = False

    for result in results['items']:
        if result['title'].lower() == movie:
            movie = result['title']
            found = True

            services = result['offers']

            for service in services:
                if service['monetization_type'] == 'flatrate':
                    if service['provider_id'] not in providersFound:
                        if service['provider_id'] in idToName:
                            providersFound.append(service['provider_id'])

    if found == True:
        msg = "You can watch " + movie + " on " + idToName[providersFound[0]]
        print(providersFound)

        for i in range(1, len(providersFound)):
            if i == len(providersFound) - 1:
                msg += " and " + idToName[providersFound[i]]
            else:
                msg += ", " + idToName[providersFound[i]]

        msg += "."

        return responseWithCard(msg, movie)

    else:
        return responseWithCard("Sorry. I couldn't find any streaming services for " + movie)

def cancelIntent():
    return build_response("")

def helpIntent():
    return build_response("You can say something like: Ask Stream Finder where I can watch The Office")

def stopIntent():
    return build_response("Goodbye!")

def onLaunch():
    

def lambda_handler(event, context):
    intent_name = event['request']['intent']['name']
    just_watch = JustWatch(country='US')

    print(event['request'])

    if intent_name == 'SearchTV':
        return handleTV(event, just_watch)
    elif intent_name == 'SearchMovie':
        return handleMovies(event, just_watch)
    elif intent_name == 'Cancel':
        cancelIntent()
    elif intent_name == 'Help':
        helpIntent()
    elif intent_name == 'Stop':
        stopIntent()
    elif intent_name == 'Launch':
        onLaunch()

