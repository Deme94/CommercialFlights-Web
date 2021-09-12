import requests
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import TruncatedSVD
import pickle
import os

def clasificar():
  dir_path = os.path.dirname(__file__)


  # import warnings filter
  from warnings import simplefilter
  # ignore warnings
  simplefilter(action='ignore', category=FutureWarning)
  pd.set_option('mode.chained_assignment', None)

  print('Extrayendo vuelos programados a predecir...')
  #Clasificacion--------------------------------------------------------------------------------------
      # Obtencion de datos de entrenamiento de la BBDD
  jsonOriginal = requests.get('http://127.0.0.1:8000/api/vuelos/predecir/0').json()
  print('Haciendo predicciones de los vuelos programados...')

  # Montamos el dataframe (tabla) sobre el que se va a trabajar
  df = pd.DataFrame(columns=[
              'id_vuelo',
              'id_aerolinea',
              'id_aeropuerto_salida',
              'mes',
              'aeropuerto_destino',
              'codigo_vuelo',
              'terminal',
              'distancia',
              'hora_programada',
              'cielo',
              'temperatura',
              'lluvia',
              'porcentajeLluvia',
              'nubes',
              'viento',
              'rafaga',
              'direccion_viento',
              'humedad',
              'presion'
              ])

  for vuelo in jsonOriginal:
      # De la fecha solo queremos entrenar con el mes, y las horas las pasamos a decimal para un mejor aprendizaje
      mes = int(vuelo['date_time'].split('-')[1])
      hora_programada_decimal = float(vuelo['hora_programada'].split(':')[0]) + float(vuelo['hora_programada'].split(':')[1])/60
      
      # Añadimos fila a fila
      df.loc[-1] = [
             vuelo['id_vuelo'],
             vuelo['id_aerolinea'],
             vuelo['id_aeropuerto_salida'],
             mes,
             vuelo['aeropuerto_destino'],
             vuelo['codigo_vuelo'],
             vuelo['terminal'],
             vuelo['distancia'],
             hora_programada_decimal,
             vuelo['cielo'],
             vuelo['temperatura'],
             vuelo['lluvia'],
             vuelo['porcentajeLluvia'],
             vuelo['nubes'],
             vuelo['viento'],
             vuelo['rafaga'],
             vuelo['direccion_viento'],
             vuelo['humedad'],
             vuelo['presion']
             ]
      df.index = df.index + 1  # shifting index
      
  df = df.sort_index()  # sorting by index

  # Definimos el tipo de dato de columna y actualizamos nuestro dataframe
  caracteristicas_numericas = df[['distancia','hora_programada','temperatura','lluvia','porcentajeLluvia','nubes','viento',
                                  'rafaga','humedad','presion']]
  for columna in caracteristicas_numericas.columns:
      caracteristicas_numericas[columna] = caracteristicas_numericas[columna].astype(float)
      
  caracteristicas_categoricas = df[['id_aerolinea','id_aeropuerto_salida','mes','aeropuerto_destino','codigo_vuelo','terminal',
                                   'cielo','direccion_viento']]

  for columna in caracteristicas_categoricas.columns:
      caracteristicas_categoricas[columna] = caracteristicas_categoricas[columna].astype(str)

  df = pd.concat([df['id_vuelo'],caracteristicas_numericas, caracteristicas_categoricas], axis=1)
  print(df)  

  model = pickle.load(open(dir_path+'model.sav', 'rb'))

  X_test = df
  horas_estimadas = model.predict(X_test)

  i=0
  diccionario = {}
  for idVuelo in X_test['id_vuelo']:
      hora = str(horas_estimadas[i]).split('.')[0]
      hora = int(hora)
      if(hora>23):
          hora = hora-24
      hora = str(hora)
      if(len(hora)==1):
          hora = '0'+hora
      minutos = str(int(round(float('0.'+str(horas_estimadas[i]).split('.')[1])*60)))
      if(len(minutos)==1):
          minutos = '0'+minutos
      hora_estimada = hora+':'+minutos
      diccionario[idVuelo] = hora_estimada
      print('Id:',idVuelo,'| Hora Programada:',X_test['hora_programada'][i],'| Hora Estimada:', horas_estimadas[i])
      i = i+1

  requests.post('http://127.0.0.1:8000/api/vuelos/estimaciones', json = diccionario)

if __name__ == "__main__":
    clasificar()