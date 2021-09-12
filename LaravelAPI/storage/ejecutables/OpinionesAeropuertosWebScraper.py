import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import SentimentAnalysis
import JSONWriteRead
import os

dir_path = os.path.dirname(__file__)

def recopilar():
    print("\nRecopilando opiniones de los aeropuertos...")
    
    # Abre el navegador y accede a la URL
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options,executable_path=dir_path+'/geckodriver.exe')
    
    # Arrays de rutas de aeropuertos que se van a recopilar, así como los códigos de los aeropuertos
    URLS = [
            'https://www.flightradar24.com/data/airports/mad/reviews',      
            'https://www.flightradar24.com/data/airports/sxf/reviews',
            'https://www.flightradar24.com/data/airports/jed/reviews',
            'https://www.flightradar24.com/data/airports/aep/reviews',
            'https://www.flightradar24.com/data/airports/cbr/reviews',
            'https://www.flightradar24.com/data/airports/gru/reviews',
            'https://www.flightradar24.com/data/airports/yyz/reviews',
            'https://www.flightradar24.com/data/airports/pek/reviews',
            'https://www.flightradar24.com/data/airports/icn/reviews',
            'https://www.flightradar24.com/data/airports/atl/reviews',
            'https://www.flightradar24.com/data/airports/cdg/reviews',
            'https://www.flightradar24.com/data/airports/del/reviews',
            'https://www.flightradar24.com/data/airports/cgk/reviews',
            'https://www.flightradar24.com/data/airports/fco/reviews',
            'https://www.flightradar24.com/data/airports/nrt/reviews',
            'https://www.flightradar24.com/data/airports/mex/reviews',
            'https://www.flightradar24.com/data/airports/lhr/reviews',
            'https://www.flightradar24.com/data/airports/dme/reviews',
            'https://www.flightradar24.com/data/airports/jnb/reviews',
            'https://www.flightradar24.com/data/airports/isl/reviews'
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
    
    try:
        for i in range(0, len(AEROPUERTOS)):
            print('\n',AEROPUERTOS[i],'--------------------------------------------------------------------------------------------------')
            driver.get(URLS[i])
            time.sleep(5)
            WebDriverWait(driver, 30).until(  
                EC.element_to_be_clickable((By.ID,"btn-load-reviews"))
            )    
    
            
            # Obtenemos el html de la página
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            numero_opiniones_totales = int(soup.select_one('.btn-sort').text.split()[0])
            numero_opiniones_cargadas = len(soup.select('.cnt-comment .content'))
    
            print('Número de opiniones totales = ',numero_opiniones_totales)
            print('Número de opiniones cargadas = ',numero_opiniones_cargadas)
    
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
            time.sleep(1)
            
            # Bucle que mientras no se hayan cargado todas las opiniones
            c = 1
            faltanReviews = True
            while (numero_opiniones_totales != numero_opiniones_cargadas):
                print('Leer más ('+str(c)+')')
                
                leerMas = driver.find_element_by_id("btn-load-reviews")                             # Obtiene el botón de cargar más reviews   
                 
                leerMas.click()                                                                     # Click en el botón de cargar más reviews
                time.sleep(5)
                
                botonNoEncontrado = True
                # Espera a que el botón de cargar más reviews se pueda clickar
                while(faltanReviews and botonNoEncontrado):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
                    time.sleep(1)
                    try:
                        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID,"btn-load-reviews")))    
                    # Si el botón ya no se puede pulsar, comprueba que todas las opiniones se han cargado, si no (error) recarga la página y vuelta a empezar
                    except TimeoutException:
                        page_source = driver.page_source                                                    # Coge nuevo html
                        soup = BeautifulSoup(page_source, 'html.parser')                                    # Actualiza el soup
                        filas = soup.select('.cnt-comment .content')
                        numero_opiniones_cargadas = len(filas)
                        if(numero_opiniones_totales != numero_opiniones_cargadas):
                            print('Error botón Leer más (no ha cargado).\nReiniciando página...')   
                            c=0
                            driver.refresh()
                            time.sleep(5)
                        else:
                            faltanReviews = False
                    botonNoEncontrado = False
                        
                page_source = driver.page_source                                                    # Coge nuevo html
                soup = BeautifulSoup(page_source, 'html.parser')                                    # Actualiza el soup
                # Seleccionamos todos los comentarios con select, quedan en un array
                filas = soup.select('.cnt-comment .content')
                numero_opiniones_cargadas = len(filas)
                print('Opiniones cargadas = ',numero_opiniones_cargadas,'/',numero_opiniones_totales)
                c+=1
            
            print('Extrayendo opiniones y calculando sus compound...')
            
            opiniones = []
            # Almacenamos el texto de cada comentario en el array de opiniones
            for fila in filas:
                compound = SentimentAnalysis.analizar_string(SentimentAnalysis.detectAndTransalate(fila.text.replace('\'','')))
                opinion = {
                    'opinion': fila.text,
                    'compound': compound,
                    }
                opiniones.append(opinion)
            
            print(opiniones)     
            diccionario[AEROPUERTOS[i]] = opiniones
        
        print('\n******************************* FIN SCRAPER *******************************')
        print('\nDICCIONARIO CON OPINIONES DE TODOS LOS AEROPUERTOS =',diccionario)
        
        # Cierra el navegador
        driver.close()
        
        return diccionario
    except:
        driver.save_screenshot('errorReviews.png')
        # Cierra el navegador
        driver.close()

# Función main en caso de que se ejecute este script, para comprobar los resultados
if __name__ == "__main__":
    opinionesAeropuertos = recopilar()
    JSONWriteRead.escribirJSON(opinionesAeropuertos, 'reviews_aeropuertos')
