import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import JSONWriteRead
import requests


# Clase del scraper de vuelos, en el init se ejecuta todo el scraping para una fecha y estado de vuelos
class VuelosScraper:
    def __init__(self, fecha, estados):
        print('\nRecopilando datos de vuelos...')
        self.fecha = fecha

        # Navegador de chrome (selenium)
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

        # Arrays de rutas de aeropuertos que se van a recopilar, así como los códigos de los aeropuertos
        URLS = [
                'https://www.airportia.com/spain/madrid-barajas-international-airport/departures/',
                'https://www.airportia.com/germany/berlin_sch%c3%b6nefeld-international-airport/departures/',
                'https://www.airportia.com/saudi-arabia/king-abdulaziz-international-airport/departures/',
                'https://www.airportia.com/argentina/jorge-newbery-airpark-airport/departures/',
                'https://www.airportia.com/australia/canberra-international-airport/departures/',
                'https://www.airportia.com/brazil/guarulhos-_-governador-andr%C3%A9-franco-montoro-international-airport/departures/',
                'https://www.airportia.com/canada/lester-b.-pearson-international-airport/departures/',
                'https://www.airportia.com/china/beijing-capital-international-airport/departures/',
                'https://www.airportia.com/south-korea/incheon-international-airport/departures/',
                'https://www.airportia.com/united-states/hartsfield-jackson-atlanta-international-airport/departures/',
                'https://www.airportia.com/france/charles-de-gaulle-international-airport/departures/',
                'https://www.airportia.com/india/indira-gandhi-international-airport/departures/',
                'https://www.airportia.com/indonesia/soekarno_hatta-international-airport/departures/',
                'https://www.airportia.com/italy/leonardo-da-vinci/departures/',
                'https://www.airportia.com/japan/narita-international-airport/departures/',
                'https://www.airportia.com/mexico/licenciado-benito-juarez-international-airport/departures/',
                'https://www.airportia.com/united-kingdom/london-heathrow-airport/departures/',
                'https://www.airportia.com/russia/domodedovo-international-airport/departures/',
                'https://www.airportia.com/south-africa/or-tambo-international-airport/departures/'
#                'https://www.airportia.com/turkey/atat%C3%BCrk-international-airport/departures/'                
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
                'JNB'      # SUDÁFRICA-JOHANNESBURGO
 #               'ISL'      # TURQUÍA-ESTAMBUL-YESILKOY 
                ]

        self.diccionario = {}
        
        try:
            for i in range(0, len(AEROPUERTOS)):
                print('\n',AEROPUERTOS[i],'--------------------------------------------------------------------------------------------------')
                self.vuelos = []

                if(i%3==0):
                    print('Reiniciando navegador para mejor rendimiento...')
                    self.driver.close()
                    time.sleep(1)
                    self.driver = webdriver.Firefox(options=options)
                    
                self.driver.get(URLS[i])
                time.sleep(10)
                WebDriverWait(self.driver, 30).until(  
                        EC.element_to_be_clickable((By.CLASS_NAME,"flightsTable-track"))
                )
                if(i%3==0):
                    try:
                        self.driver.find_element_by_class_name("qc-cmp-button").click()
                    except:
                        print();
                    #time.sleep(1)
                
                intentos = 0
                while True:
                    try:
                        # Recopilamos los vuelos de la tabla
                        self.__irDia(fecha.replace('-',''))
                        for estado in estados:
                            self.__extraerVuelos(estado)    
                    except Exception as e:
                        if intentos < 2:
                            print(e)            
                            self.driver.refresh()
                            time.sleep(10)
                            intentos = intentos + 1
                            continue;
                    intentos = 0
                    break;
     
                
                print('Vuelos =',self.vuelos)
                if(len(self.vuelos) > 0):
                    self.diccionario[AEROPUERTOS[i]] = self.vuelos
            
            print('\n*********************************  FIN SCRAPER *******************************')
            print('\nDICCIONARIO TODOS LOS AEROPUERTOS Y VUELOS =',self.diccionario)
            
            # Cierra el navegador
            self.driver.close() 
        except Exception as e:
            print(e)
            self.driver.save_screenshot('errorAirportia.png')
            # Cierra el navegador
            self.driver.close()
    
    def getDiccionario(self):
        return self.diccionario
        
    # Navega al día elegido de la página
    def __irDia(self, fecha):
        print()
        print('Extrayendo datos del día',fecha,'...')
        #self.driver.execute_script("window.scrollTo(0, 200)")  
        #time.sleep(1)          
        # Seleccionamos la fecha
        select = self.driver.find_element_by_class_name("flightsFilter-select--date")
        option = select.find_element_by_css_selector('option[value="'+fecha+'"]')
        print('Click fecha')
        option.click()
        #time.sleep(1)
        # Seleccionamos la hora de inicio
        select = self.driver.find_element_by_class_name("flightsFilter-select--fromTime")
        options = select.find_elements_by_tag_name('option')
        print('Click hora inicio')
        options[0].click()
        #time.sleep(1)
        # Seleccionamos la hora de fin
        select = self.driver.find_element_by_class_name("flightsFilter-select--toTime")
        options = select.find_elements_by_tag_name('option')
        print('Click hora fin')
        options[len(options)-1].click()
        #time.sleep(1)
        # Hacemos click en GO y cargamos la nueva página con el día elegido
        print('Click GO')
        self.driver.find_element_by_class_name("flightsFilter-submit").click()
        #time.sleep(5)
        time.sleep(3)
        WebDriverWait(self.driver, 30).until(  
                EC.element_to_be_clickable((By.CLASS_NAME,"flightsTable-track"))
        )                                             
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
        #time.sleep(1)
    
    # Recopila todos los datos de los vuelos de la página y los guarda en un diccionario
    def __extraerVuelos(self, estado):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        trs = soup.select('tr')
        # Cada fila
        for tr in trs:
            # Filtra las filas de los vuelos
            if(estado in tr.text and 'Track' in tr.text):
                tds = tr.select('td')
                # Extraemos cada dato del vuelo dentro de la fila
                codigoVuelo = tds[0].text.split()[0]
                destino = tds[1].text.split()[-1]
                aerolinea = tds[2].text
                horaProgramada = tds[3].text
                horaReal = tds[4].text
                if estado == 'Scheduled':
                    estadoVuelo = 0
                else:
                    if horaReal == '':
                        continue;
                    estadoVuelo = 1
                # Navegamos a la página específica de cada vuelo
                linkVuelo = tds[6].a['href']
                while True:
                    try:  
                        self.driver.find_element_by_css_selector('a[href="'+linkVuelo+'"]').click()
                        #time.sleep(3)
                        WebDriverWait(self.driver, 30).until(  
                                EC.element_to_be_clickable((By.CLASS_NAME,"airportiaMap"))
                        ) 
                        page_source = self.driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')
                        # Extraemos los datos que faltan
                        try:
                            terminal = soup.select_one('.flightInfo-misc').text.split()[1]
                        except:
                            terminal = ''
                        distancia = soup.select_one('.flightInfo-distance').text.split()[1]
                        
                        print('Fecha: ',self.fecha)
                        print('Código vuelo: ',codigoVuelo)
                        print('Destino: ',destino)   
                        print('Aerolinea: ',aerolinea)
                        print('Hora programada: ',horaProgramada)
                        print('Hora real: ',horaReal)
                        print('Estado: ',estadoVuelo)
                        print('Terminal:',terminal)
                        print('Distancia (km): ',distancia)
                        
                        vuelo = {
                                'fecha':self.fecha,
                                'codigoVuelo':codigoVuelo,
                                'destino':destino,
                                'aerolinea':aerolinea,
                                'horaProgramada':horaProgramada,
                                'horaReal':horaReal,
                                'estado':estadoVuelo,
                                'terminal':terminal,
                                'distancia':distancia
                                }
                        self.vuelos.append(vuelo)
                        print('Vuelo =',vuelo,'\n')
                        # Navegamos atrás para volver a la página de los vuelos
                        self.driver.execute_script("window.history.go(-1)")
                        #time.sleep(3)
                        WebDriverWait(self.driver, 30).until(  
                                EC.element_to_be_clickable((By.CLASS_NAME,"compensationLink"))
                        ) 
                        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
                        #time.sleep(1)
                        page_source = self.driver.page_source
                        soup = BeautifulSoup(page_source, 'html.parser')   
                    except Exception as e:
                        print(e)
                        self.driver.save_screenshot('errorAirportia.png')
                        self.__irDia(self.fecha.replace('-',''))
                        #time.sleep(3)
                        WebDriverWait(self.driver, 30).until(  
                                EC.element_to_be_clickable((By.CLASS_NAME,"compensationLink"))
                        ) 
                        continue;
                    break;

# Recopila los vuelos de ayer que han salido
def recopilarAyer():
    valorFecha_Ayer = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')  
    estados = ['Landed', 'En-Route']                
    vuelos = VuelosScraper(valorFecha_Ayer, estados)
    return vuelos.getDiccionario()
# Recopila los vuelos de hoy que están programados
def recopilarHoy():
    valorFecha_Hoy = datetime.strftime(datetime.now(), '%Y-%m-%d')     
    estados = ['Scheduled', 'Landed', 'En-Route']                             
    vuelos = VuelosScraper(valorFecha_Hoy, estados)
    return vuelos.getDiccionario()

# Función main en caso de que se ejecute este script, para comprobar los resultados
if __name__ == "__main__":
    vuelosAyer = recopilarAyer()
    requests.post('http://127.0.0.1:8000/api/vuelos', json = vuelosAyer)
    
    vuelosHoy = recopilarHoy()
    requests.post('http://127.0.0.1:8000/api/vuelos', json = vuelosHoy)
    
    