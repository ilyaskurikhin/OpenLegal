import requests


path = "entscheide.txt"
with open(path, "r") as file:
    Entscheidungen = file.read().splitlines()


def API_getInfos(url):
    response = requests.get(url)
    return response


for entsch in Entscheidungen:
    entscheidungen = entsch#.replace(" ", "-")
    url = "https://bger.li/" + entscheidungen
    response = API_getInfos(url)
    with open('output/' + entscheidungen + ".html", "w", encoding='UTF-8') as file:
        file.write(response.text)
        file.close()

"""
for x in range(30):
    url = "https://bger.li/138 I " + str(x)
    response = API_getInfos(url)
    with open('output/138 I ' + str(x) + ".html", "w", encoding="UTF-8") as file:
        file.write(response.text)
        file.close()
"""
