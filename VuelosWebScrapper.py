import asyncio
from bs4 import BeautifulSoup
from pyppeteer import launch


# Función main asíncrona
async def main():
    # Abre el navegador, una ventana y accede a la URL
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.airportia.com/widgets/airport/mad/departures/?df=dmy')
    # Obtenemos el html de la página
    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')
    filas = soup.select('tr', class_='flightsTable-parentFlight')
    vuelos = []
    for fila in filas:
        vuelos.append(fila.text)

    vuelosFinal = []
    for vuelo in vuelos:
        vueloAux = vuelo.split()
        for i in [0,1,2,3,4]:
            if i<4:
                vuelosFinal.append(vueloAux[i])
                # vuelosFinal.append(',')
            else:
                vuelosFinal.append(vueloAux[i])
        #vuelosFinal.append(';')

    # for vuelo in vuelosFinal:
        # print(vuelo)
    diccionario = {'MAD': vuelosFinal}

    print(diccionario)

    # Cierra el navegador
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
