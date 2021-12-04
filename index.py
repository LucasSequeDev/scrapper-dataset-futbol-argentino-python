from Torneos import Torneos

from bs4 import BeautifulSoup
import requests
import pandas as pd

dataSet = []
partidosSinDatos = 0
partidosConDatos = 0

for Torneo in Torneos:
    page = requests.get(Torneo['url'])
    content = page.content

    soup = BeautifulSoup(content, "html.parser")

    jornadas = soup.find_all(id='col-resultados')



    for jornada in jornadas:
        jornadaCompleta = jornada.find(class_='titlebox').text

        tablaJornada = jornada.find('table')
        partidosJornada = tablaJornada.find_all('tr')

        for partido in partidosJornada:
            data = partido.find_all('td')
            if len(data) > 0:
                fechaPartido = data[0].text.strip()
                equipoLocal = data[1].find('img').get('alt').strip()
                resultado = data[2].find('a').text.strip()
                equipoVisitante = data[3].find('img').get('alt').strip()

                try:
                    equipoLocalResultad = resultado.split('-')[0].strip()
                    equipoVisitanteResultado = resultado.split('-')[1].strip()
                except:
                    equipoLocalResultad = '-'
                    equipoVisitanteResultado = '-'
                    


                dataSet.append({
                    'Torneo': Torneo['nombre'],
                    'jornadaCompleta': jornadaCompleta,
                    'jornadaNumero': jornadaCompleta.split(' ')[1].strip(),
                    'fechaPartido': fechaPartido,
                    'diaFechaPartido': fechaPartido.split(' ')[0].strip(),
                    'mesFechaPartido': fechaPartido.split(' ')[1].strip(),
                    'anoFechaPartido': fechaPartido.split(' ')[2].strip(),
                    'equipoLocal': equipoLocal,
                    'equipoLocalResultado': equipoLocalResultad,
                    'equipoVisitante': equipoVisitante,
                    'equipoVisitanteResultado': equipoVisitanteResultado,
                    'resultado': str(equipoLocalResultad) + '-' + str(equipoVisitanteResultado)
                })
                partidosConDatos += 1
            else:
                partidosSinDatos += 1

            
print(f'Partidos con datos: {partidosConDatos}')
print(f'Partidos sin datos: {partidosSinDatos}')
# print(content)

df = pd.DataFrame(dataSet)

print(df.head())

df.to_csv('dataset_torneos_futbol_argentino.csv', encoding='utf-8')