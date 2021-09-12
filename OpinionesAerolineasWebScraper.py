from bs4 import BeautifulSoup
import urllib.request
import requests
import SentimentAnalysis
import JSONWriteRead

def cargar_html():

    #URLs de opiniones en inglés
    url_aerolineas = "https://www.edreams.com/offers/flights/airline/"


    html = requests.get(url_aerolineas)
    soup = BeautifulSoup(html.content, 'html.parser')

    lista_links_aerolineas = []

    diccionario = {}

    # Recoge los links de cada página de cada aerolínea
    for link in soup.findAll('a', class_="odf-link"):
        lista_links_aerolineas.append(link.get('href'))
    print(lista_links_aerolineas)

    """nombres_aerolineas = soup.find_all('a', class_="odf-link")

    # Recoge los nombres de las aerolíneas
    for nombre in range(len(nombres_aerolineas)):
        nombre = nombres_aerolineas[nombre].get_text()
        lista_nombres_aerolineas.append(nombre)
    print(lista_nombres_aerolineas)"""

    #Recorre cada perfil de aerolínea recogiendo su nombre y sus reviews
    for i in lista_links_aerolineas:
        html_1 = requests.get(i)
        soup_1 = BeautifulSoup(html_1.content, 'html.parser')

        lista_reviews = []

        #Reviews
        texto_reviews = soup_1.find_all('p', class_="description reviews-list-review-resume-text")
        #Nombres
        nombre_aerolineas = soup_1.find_all('span', class_="breadcrumb-item is-current")

        for z in range(len(nombre_aerolineas)):
            name = nombre_aerolineas[z].get_text()
        print(name)
        file = open("Lista_Aerolineas.txt")
        line = file.read().replace(",", " ").replace("[", " ").replace("]", " ")
        file.close()
        #Recorremos la lista de aerolíneas general, y si no se encuentra en la lista no se almacena.
        if name in str(line):
            #print("Ejecutando...", name)
            for j in range(len(texto_reviews)):
                text = texto_reviews[j].get_text()
                compound = SentimentAnalysis.analizar_string(SentimentAnalysis.detectAndTransalate(text.replace('\'', '')))
                opinion = {
                'opinion': text,
                'compound': compound,
                }
                lista_reviews.append(opinion)
                #Almacenamos toda la información recopilada en un diccionario
            diccionario[name] = lista_reviews

            #Comprobamos si la aerolinea tiene reviews, en caso de que no tenga no la guardamos
            if len(lista_reviews) == 0:
                diccionario.pop(name)
            #print(lista_reviews)
    return diccionario

if __name__ == "__main__":
    opinionesAerolineas = cargar_html()
    JSONWriteRead.escribirJSON(opinionesAerolineas, 'reviews_aerolineas')
