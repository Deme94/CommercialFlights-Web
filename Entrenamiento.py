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
from matplotlib import pyplot as plt
import JSONWriteRead
import base64
import os

dir_path = os.path.dirname(__file__)


# import warnings filter
from warnings import simplefilter
# ignore warnings
simplefilter(action='ignore', category=FutureWarning)
pd.set_option('mode.chained_assignment', None)

print('Extrayendo vuelos de la BBDD...')
# Obtencion de datos de entrenamiento de la BBDD
jsonOriginal = requests.get('http://127.0.0.1:8000/api/vuelos/predecir/1').json()

print(len(jsonOriginal))
print('Generando modelo...')
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
            'hora_salida',
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
    hora_salida_decimal = float(vuelo['hora_salida'].split(':')[0]) + float(vuelo['hora_salida'].split(':')[1])/60
    
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
           hora_salida_decimal,
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

df = pd.concat([df['id_vuelo'],caracteristicas_numericas, caracteristicas_categoricas, df['hora_salida']], axis=1)
print(df)  
# Se crean pipelines de preprocesamiento para los tipos numericos y categoricos
transformador_numerico = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

transformador_categorico = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])
    
preprocesador = ColumnTransformer(
    transformers=[
        ('num', transformador_numerico, caracteristicas_numericas.select_dtypes(include=['int64', 'float64']).columns),
        ('cat', transformador_categorico, caracteristicas_categoricas.select_dtypes(include=['object', 'bool']).columns)])

# Completamos la pipeline de preprocesamiento con la de prediccion
clf = Pipeline(steps=[('preprocesador', preprocesador),
                ('reduce_dim', TruncatedSVD(200)),
                ('classifier', linear_model.Ridge())])

param_grid = {}

grid_search = GridSearchCV(clf, param_grid, cv=3)
# Definimos las caracteristicas y el target
X = df.drop('hora_salida', axis=1)
Y = df['hora_salida']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    
# Entrenamos el modelo y mostramos la precision
grid_search.fit(X_train, y_train)
#print(grid_search.best_params_)
pred = grid_search.predict(X_test)

score = grid_search.score(X_test, y_test)
samples = len(df['id_vuelo'])
print("Linear Regression Score: %.3f" % score) 
print("Número de samples = ",samples)

graficaReal = pd.concat([X_test['hora_programada'], y_test], axis=1)
graficaReal = graficaReal.sort_values('hora_programada')

graficaEstimada = pd.DataFrame()
graficaEstimada['hora_programada'] = X_test['hora_programada']
graficaEstimada = graficaEstimada.reset_index(drop=True)
graficaEstimada['hora_estimada'] = pd.Series(pred)
graficaEstimada = graficaEstimada.sort_values('hora_programada')

comparacion = pd.concat([X_test['hora_programada'], y_test], axis=1)
comparacion = comparacion.reset_index(drop=True)
comparacion['hora_estimada'] = pd.Series(pred)
print(comparacion)

plt.ylabel('Hora salida')
plt.xlabel('Hora programada')
fig = plt.gcf()
plt.scatter(graficaReal['hora_programada'], graficaReal['hora_salida'],color='black',s=40,alpha=0.2)
m, b = np.polyfit(graficaEstimada['hora_programada'], graficaEstimada['hora_estimada'], 1)
plt.plot(graficaEstimada['hora_programada'], m*graficaEstimada['hora_programada']+b,color='red', linewidth=3)


diccionario = {}
diccionario['score'] = score
diccionario['samples'] = samples
diccionario['x_true'] = graficaReal['hora_programada'].to_list()
diccionario['y_true'] = graficaReal['hora_salida'].to_list()
diccionario['y_pred'] = graficaEstimada['hora_estimada'].to_list()
diccionario['y_regresion'] = (m*graficaEstimada['hora_programada']+b).to_list()

pickle.dump(grid_search, open(dir_path+'model.sav', 'wb'))              # Save Model
JSONWriteRead.escribirJSON(diccionario, dir_path+'model')               # Save JSON
