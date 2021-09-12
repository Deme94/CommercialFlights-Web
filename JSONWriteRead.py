import json


def escribirJSON(data, name):
    with open(name+'.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def leerJSON(datos):
    with open(datos + '.json') as file:
        data = json.load(file)
    return data





if __name__ == '__main__':
    data = {}
    data['clients'] = []
    data['clients'].append({
        'first_name': 'Sigrid',
        'last_name': 'Mannock',
        'age': 27,
        'amount': 7.17})
    data['clients'].append({
        'first_name': 'Joe',
        'last_name': 'Hinners',
        'age': 31,
        'amount': [1.90, 5.50]})
    data['clients'].append({
        'first_name': 'Theodoric',
        'last_name': 'Rivers',
        'age': 36,
        'amount': 1.11})
    escribirJSON(data, 'cliente')
