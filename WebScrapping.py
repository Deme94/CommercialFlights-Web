import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import JSONWriteRead as JWR


# Navega al día elegido de la página
def irDia(fecha):
    print()
    print('Extrayendo datos del día', fecha, '...')
    driver.execute_script("window.scrollTo(0, 200)")
    # Seleccionamos la fecha
    select = driver.find_element_by_class_name("flightsFilter-select--date")
    option = select.find_element_by_css_selector('option[value="' + fecha + '"]')
    print('Click fecha')
    option.click()
    time.sleep(1)
    # Seleccionamos la hora de inicio
    select = driver.find_element_by_class_name("flightsFilter-select--fromTime")
    options = select.find_elements_by_tag_name('option')
    print('Click hora inicio')
    options[0].click()
    time.sleep(1)
    # Seleccionamos la hora de fin
    select = driver.find_element_by_class_name("flightsFilter-select--toTime")
    options = select.find_elements_by_tag_name('option')
    print('Click hora fin')
    options[len(options) - 1].click()
    time.sleep(1)
    # Hacemos click en GO y cargamos la nueva página con el día elegido
    print('Click GO')
    driver.find_element_by_class_name("flightsFilter-submit").click()
    time.sleep(6)  # Click en GO
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


# Recopila todos los datos de los vuelos de la página y los guarda en un diccionario
def recopilarVuelos(estado):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    trs = soup.select('tr')
    # Cada fila
    for tr in trs:
        # Filtra las filas de los vuelos
        if (estado in tr.text and 'Track' in tr.text):
            tds = tr.select('td')
            # Extraemos cada dato del vuelo dentro de la fila
            codigoVuelo = tds[0].text.split()[0]
            destino = tds[1].text.split()[-1]
            aerolinea = tds[2].text
            horaProgramada = tds[3].text
            horaReal = tds[4].text
            if estado == 'Scheduled':
                estadoVuelo = 0
                fecha = datetime.strftime(datetime.now(), '%Y-%m-%d')
            else:
                if horaReal == '':
                    continue;
                estadoVuelo = 1
                fecha = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
            # Navegamos a la página específica de cada vuelo
            linkVuelo = tds[6].a['href']
            driver.find_element_by_css_selector('a[href="' + linkVuelo + '"]').click()
            time.sleep(6)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            # Extraemos los datos que faltan
            try:
                terminal = soup.select_one('.flightInfo-misc').text.split()[1]
            except:
                terminal = '--'
            distancia = soup.select_one('.flightInfo-distance').text.split()[1]

            print('Fecha: ', fecha)
            print('Código vuelo: ', codigoVuelo)
            print('Destino: ', destino)
            print('Aerolinea: ', aerolinea)
            print('Hora programada: ', horaProgramada)
            print('Hora real: ', horaReal)
            print('Estado: ', estadoVuelo)
            print('Terminal:', terminal)
            print('Distancia (km): ', distancia)

            vuelo = {
                'fecha': fecha,
                'codigoVuelo': codigoVuelo,
                'destino': destino,
                'aerolinea': aerolinea,
                'horaProgramada': horaProgramada,
                'horaReal': horaReal,
                'estado': estadoVuelo,
                'terminal': terminal,
                'distancia': distancia
            }
            vuelos.append(vuelo)
            print(vuelo, '\n')
            # Navegamos atrás para volver a la página de los vuelos
            driver.execute_script("window.history.go(-1)")
            time.sleep(6)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')


# Recopila las opiniones de los vuelos
def opinionesAeropuertos():
    print("Recopilando opiniones de los aeropuertos...")

    # Abre el navegador y accede a la URL
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.flightradar24.com/data/airports/mad/reviews')
    time.sleep(2)

    # Obtenemos el html de la página
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Bucle que mientras el botón de "load more reviews" esté habilitado, seguirá desplegando más comentarios y cargando el nuevo contenido html
    existeBoton = True
    i = 0
    while (existeBoton):
        print('Leer más (' + str(i) + ')')
        leerMas = driver.find_element_by_id("btn-load-reviews")  # Obtiene el botón de cargar más reviews
        leerMas.click()  # Click en el botón de cargar más reviews
        time.sleep(6)  # Espera 2 segundos
        page_source = driver.page_source  # Coge nuevo html
        soup = BeautifulSoup(page_source, 'html.parser')  # Actualiza el soup
        existeBoton = (soup.select_one('#btn-load-reviews').get(
            'disabled') is None)  # Si el botón de cargar más reviews está deshabilitado; es False, si no True
        i += 1

    # Seleccionamos todos los comentarios con select, quedan en un array
    filas = soup.select('.cnt-comment .content')
    opiniones = []
    # Almacenamos el texto de cada comentario en el array de opiniones
    for fila in filas:
        opiniones.append(fila.text)

    # Generamos el diccionario con todas las opiniones del aeropuerto MAD (Madrid-Barajas)
    diccionario = {"MAD": opiniones}

    print(diccionario)
    print(len(filas))

    requests.post('http://127.0.0.1:8000/api/aeropuertos/reviews', json=diccionario)

    # Cierra el navegador
    driver.close()
    return diccionario


if __name__ == '__main__':
    # ------------------------------------Scrapping vuelos--------------------------------------------------------------
    # Abre el navegador, una ventana y accede a la URL
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.airportia.com/spain/madrid-barajas-international-airport/departures/')
    time.sleep(5)

    vuelos = []

    # Recopilamos los vuelos de ayer
    valorFecha_Ayer = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
    irDia(valorFecha_Ayer)
    recopilarVuelos('Landed')
    recopilarVuelos('En-Route')
    # Recopilamos los vuelos de hoy
    valorFecha_Hoy = datetime.strftime(datetime.now(), '%Y%m%d')
    irDia(valorFecha_Hoy)
    recopilarVuelos('Scheduled')
    print(vuelos)

    # requests.post('http://127.0.0.1:8000/api/aeropuertos/reviews', json = diccionario)

    # Cierra el navegador
    driver.close()
    JWR.escribirJSON(vuelos, 'vuelos') # escribimos el JSON vuelos

    # ------------------------------------Scrapping opiniones aeropuertos-----------------------------------------------
    JWR.escribirJSON(opinionesAeropuertos(), 'opinionesAeropuertos') # escribimos el JSON opiniones aeropuertos

    # ------------------------------------Scrapping Clima---------------------------------------------------------------

