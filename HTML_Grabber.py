import requests


Entscheidungen = ["141 II 272",
    "141 III 59",
    "141 IV 266",
    "141 IV 400",
    "141 V 28",
    "142 II 395",
    "142 III 449",
    "142 IV 110",
    "142 V 306",
    "143 II 215",
    "143 II 690",
    "143 IV 54",
    "143 IV 125",
    "143 V 119",
    "144 I 251",
    "144 II 329",
    "144 IV 246",
    "144 V 147",
    "145 I 35",
    "145 II 271",
    "145 II 333",
    "145 III 334",
    "145 IV 18",
    "145 IV 322",
    "145 V 6",
    "146 II 116",
    "146 II 208",
    "146 III 67",
    "146 III 218",
    "146 IV 252",
    "146 V 63",
    "147 I 250",
    "147 II 28",
    "147 III 221",
    "147 V 58"]

def API_getInfos(url):

    response = requests.get(url)
    return response

for entsch in Entscheidungen:
    entscheidungen = entsch.replace(" ", "-")
    url="https://bger.li/"+entscheidungen
    response = API_getInfos(url)
    with open('output/' + entscheidungen+".html", "x", encoding='UTF-8') as file:
        file.write(response.text)
        file.close()

