#!/usr/bin/env python 
import VuelosAirportiaWebScraper
import OpinionesAeropuertosWebScraper
import ClimaWebScraper
import OpinionesAerolineasWebScraper
import requests
import JSONWriteRead
import Clasificacion

clima = ClimaWebScraper.recopilar()
print(requests.post('http://127.0.0.1:8000/api/clima', json = clima))

vuelosAyer = VuelosAirportiaWebScraper.recopilarAyer()
requests.post('http://127.0.0.1:8000/api/vuelos', json = vuelosAyer)

vuelosHoy = VuelosAirportiaWebScraper.recopilarHoy()
requests.post('http://127.0.0.1:8000/api/vuelos', json = vuelosHoy)

Clasificacion.clasificar()
#opinionesAerolineas = OpinionesAerolineasWebScraper.cargar_html()
#JSONWriteRead.escribirJSON(opinionesAerolineas, 'reviews_aerolineas')

# Sube las opiniones de los aeropuertos (solo lo subimos 1 vez a la BBDD, no se suelen actualizar mucho)
#data = JSONWriteRead.leerJSON('reviews_aeropuertos')
#requests.post('http://127.0.0.1:8000/api/aeropuertos/reviews', json = data)

