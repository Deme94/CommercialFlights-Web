from datetime import datetime
from bs4 import BeautifulSoup
import requests
import JSONWriteRead
import sys

def recopilar():
    print('Recopilando clima de HOY...')
    # Arrays de rutas de aeropuertos que se van a recopilar, así como los códigos de los aeropuertos
    URLS = [
            'https://www.worldweatheronline.com/barajas-madrid-weather/madrid/es.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/schonefeld-weather/brandenburg/de.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/jeddah-weather/makkah/sa.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/buenos-aires-weather/distrito-federal/ar.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/canberra-weather/australian-capital-territory/au.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/guarulhos-weather/sao-paulo/br.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/toronto-weather/ontario/ca.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/peking-weather/beijing/cn.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/incheon-weather/kr.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/atlanta-weather/georgia/us.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/paris-weather/ile-de-france/fr.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/delhi-weather/delhi/in.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/tangerang-weather/banten/id.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/fiumicino-weather/lazio/it.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/narita-weather/chiba/jp.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/venustiano-carranza-weather/the-federal-district/mx.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/hillingdon-weather/hillingdon-greater-london/gb.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/moscow-weather/moscow-city/ru.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/johannesburg-weather/gauteng/za.aspx?day=0&tp=1',
            'https://www.worldweatheronline.com/yesilkoy-weather/istanbul/tr.aspx?day=0&tp=1'            
            ]
    AEROPUERTOS = [
                    'MAD',      # ESPAÑA-MADRID-BARAJAS
                    'SFX',      # ALEMANIA-BERLIN-SCHONEFELD
                    'JED',      # ARABIA SAUDITA-YEDA
                    'AEP',      # ARGENTINA-BUENOS AIRES
                    'CBR',      # AUSTRALIA-CANBERRA
                    'GRU',      # BRASIL-GUARULHOS
                    'YYZ',      # CANADA-TORONTO
                    'PEK',      # CHINA-PEKIN
                    'ICN',      # COREA DEL SUR-INCHEON
                    'ATL',      # EEUU-ATLANTA
                    'CDG',      # FRANCIA-PARIS
                    'DEL',      # INDIA-DELHI
                    'CGK',      # INDONESIA-BANTEN-TANGERANG
                    'FCO',      # ITALIA-ROMA-FIUMICINO
                    'NRT',      # JAPON-TOKYO-NARITA
                    'MEX',      # MEXICO-CIUDAD DE MEXICO-VENUSTIANO CARRANZA
                    'LHR',      # REINO UNIDO-LONDRES-HILLINGDON
                    'DME',      # RUSIA-MOSCÚ
                    'JNB',      # SUDÁFRICA-JOHANNESBURGO
                    'ISL'      # TURQUÍA-ESTAMBUL-YESILKOY 
                    ]
    diccionario = {}
    
    fecha_Hoy = datetime.strftime(datetime.now(), '%Y-%m-%d')

    for i in range(0, len(AEROPUERTOS)):
        print('\n',AEROPUERTOS[i],'--------------------------------------------------------------------------------------------------')
        page = requests.get(URLS[i])
        soup = BeautifulSoup(page.text, 'html.parser')
        tabla = soup.select_one('div.row.text-center')
        campos = soup.select('div.col.mr-1')
        horas = []
        for j in range(1, 25):
            horaClima = {
                    'fecha':fecha_Hoy,
                    'hora':campos[0+j*12-j+1].text,
                    'cielo':campos[1+j*12-j+1].text,
                    'temperatura':campos[2+j*12-j+1].text.split()[0],
                    'lluvia':campos[6+j*12-j+1].text.split()[0],
                    'porcentajeLluvia':campos[7+j*12-j+1].text.replace('%',''),
                    'nubes':campos[9+j*12-j+1].text.replace('%',''),
                    'viento':campos[4+j*12-j+1].text.split()[0],
                    'rafaga':"0",
                    'direccionViento':"null",
                    'humedad':campos[8+j*12-j+1].text.replace('%',''),
                    'presion':campos[10+j*12-j+1].text.split()[0]
                    }
            horas.append(horaClima)
            print('\nfecha: ',fecha_Hoy)
            print('hora: ',campos[0+j*12-j+1].text)
            print('cielo: ',campos[1+j*12-j+1].text)
            print('temperatura: ',campos[2+j*12-j+1].text.split()[0])
            print('lluvia: ',campos[6+j*12-j+1].text.split()[0])
            print('porcentajeLluvia: ',campos[7+j*12-j+1].text.replace('%',''))
            print('nubes: ',campos[9+j*12-j+1].text.replace('%',''))
            print('viento: ',campos[4+j*12-j+1].text.split()[0])
            print('rafaga: ',"0")
            print('direccionViento: ',"null")
            print('humedad: ',campos[8+j*12-j+1].text.replace('%',''))
            print('presion: ',campos[10+j*12-j+1].text.split()[0])
            print('horaClima =',horaClima)
            
        diccionario[AEROPUERTOS[i]] = horas
    print('\n*********************************  FIN SCRAPER *******************************')
    print('\nDICCIONARIO TODOS LOS AEROPUERTOS Y VUELOS =',diccionario)

    return diccionario

# Función main en caso de que se ejecute este script, para comprobar los resultados
if __name__ == "__main__":
    clima = recopilar()
    requests.post('http://127.0.0.1:8000/api/clima', json = clima)
    #JSONWriteRead.escribirJSON(clima, 'clima')

