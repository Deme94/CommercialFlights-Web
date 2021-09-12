from bs4 import BeautifulSoup
import urllib.request
import requests
import SentimentAnalysis
import JSONWriteRead

def cargar_html():

    #URLs de opiniones en español y castellano
    url_aerolineas = "https://www.edreams.com/offers/flights/airline/"


    html = requests.get(url_aerolineas)
    soup = BeautifulSoup(html.content, 'html.parser')

    lista_links_aerolineas = []
    lista_nombres_aerolineas = []

    # Recoge los links de cada página de cada aerolínea
    for link in soup.findAll('a', class_="odf-link"):
        lista_links_aerolineas.append(link.get('href'))
    #print(lista_links_aerolineas)

    nombres_aerolineas = soup.find_all('a', class_="odf-link")

    # Recoge los nombres de las aerolíneas
    for nombre in range(len(nombres_aerolineas)):
        nombre = nombres_aerolineas[nombre].get_text()
        lista_nombres_aerolineas.append(nombre)
    #print(lista_nombres_aerolineas)

    diccionario = {}

    for i in lista_links_aerolineas:
        html_1 = requests.get(i)
        soup_1 = BeautifulSoup(html_1.content, 'html.parser')

        lista_reviews = []

        texto_reviews = soup_1.find_all('p', class_="description reviews-list-review-resume-text")

        for j in range(len(texto_reviews)):
            text = texto_reviews[j].get_text()
            compound = SentimentAnalysis.analizar_string(SentimentAnalysis.detectAndTransalate(text.replace('\'', '')))
            opinion = {
                'opinion': text,
                'compound': compound,
            }
            lista_reviews.append(opinion)

            for k in range(len(lista_nombres_aerolineas)):
                diccionario[lista_nombres_aerolineas[k]] = lista_reviews
        #print(lista_reviews)
    #print(diccionario)
    return diccionario

if __name__ == "__main__":
    opinionesAerolineas = cargar_html()
    JSONWriteRead.escribirJSON(opinionesAerolineas, 'reviews_aerolineas')
