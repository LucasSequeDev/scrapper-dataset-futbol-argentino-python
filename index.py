from Torneos import Torneos

from bs4 import BeautifulSoup
import requests
import pandas as pd

dataSetPartidos = []
partidosSinDatos = 0
partidosConDatos = 0

for Torneo in Torneos:
    dataSetPosiciones = []
    page = requests.get(Torneo['url'])
    content = page.content

    soup = BeautifulSoup(content, "html.parser")

    jornadas = soup.find_all(id='col-resultados')

    dataPosiciones = {}
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
                    equipoLocalResultado = resultado.split('-')[0].strip()
                    equipoVisitanteResultado = resultado.split('-')[1].strip()
                except:
                    equipoLocalResultado = '-'
                    equipoVisitanteResultado = '-'

                if dataPosiciones.get(equipoLocal) is None:
                    dataPosiciones[equipoLocal] = {'equipo': equipoLocal,
                                                    'puntos': 0,
                                                    'golesFavor': 0,
                                                    'golesEnContra': 0,
                                                    'partidos': 0,
                                                    'ganados': 0,
                                                    'empatados': 0,
                                                    'perdidos': 0,
                                                    'diferenciaGoles': 0,
                                                    'ganadosLocal': 0,
                                                    'ganadosVisitante': 0,
                                                    'empatadosLocal': 0,
                                                    'empatadosVisitante': 0,
                                                    'perdidosLocal': 0,
                                                    'perdidosVisitante': 0}

                if dataPosiciones.get(equipoVisitante) is None:
                    dataPosiciones[equipoVisitante] = {'equipo': equipoVisitante,
                                                        'puntos': 0,
                                                        'golesFavor': 0,
                                                        'golesEnContra': 0,
                                                        'partidos': 0,
                                                        'ganados': 0,
                                                        'empatados': 0,
                                                        'perdidos': 0,
                                                        'diferenciaGoles': 0,
                                                        'ganadosLocal': 0,
                                                        'ganadosVisitante': 0,
                                                        'empatadosLocal': 0,
                                                        'empatadosVisitante': 0,
                                                        'perdidosLocal': 0,
                                                        'perdidosVisitante': 0}

                if equipoLocalResultado != '-':
                    if equipoLocalResultado > equipoVisitanteResultado:
                        dataPosiciones[equipoLocal]['puntos'] += 3
                        dataPosiciones[equipoLocal]['ganados'] += 1
                        dataPosiciones[equipoVisitante]['perdidos'] += 1
                        dataPosiciones[equipoLocal]['ganadosLocal'] += 1
                        dataPosiciones[equipoVisitante]['perdidosVisitante'] += 1

                    elif equipoLocalResultado == equipoVisitanteResultado:
                        dataPosiciones[equipoLocal]['puntos'] += 1
                        dataPosiciones[equipoVisitante]['puntos'] += 1
                        dataPosiciones[equipoLocal]['empatados'] += 1
                        dataPosiciones[equipoVisitante]['empatados'] += 1
                        dataPosiciones[equipoLocal]['empatadosLocal'] += 1
                        dataPosiciones[equipoVisitante]['empatadosVisitante'] += 1
                    else:
                        dataPosiciones[equipoVisitante]['puntos'] += 3
                        dataPosiciones[equipoVisitante]['perdidos'] += 1
                        dataPosiciones[equipoLocal]['ganados'] += 1
                        dataPosiciones[equipoLocal]['perdidosLocal'] += 1
                        dataPosiciones[equipoVisitante]['ganadosVisitante'] += 1

                        
                    dataPosiciones[equipoLocal]['golesFavor'] += int(equipoLocalResultado)
                    dataPosiciones[equipoLocal]['golesEnContra'] += int(equipoVisitanteResultado)
                    dataPosiciones[equipoLocal]['partidos'] += 1

                    dataPosiciones[equipoVisitante]['golesFavor'] += int(equipoVisitanteResultado)
                    dataPosiciones[equipoVisitante]['golesEnContra'] += int(equipoLocalResultado)
                    dataPosiciones[equipoVisitante]['partidos'] += 1


                dataSetPartidos.append({
                    'Torneo': Torneo['nombre'],
                    'jornadaCompleta': jornadaCompleta,
                    'jornadaNumero': jornadaCompleta.split(' ')[1].strip(),
                    'fechaPartido': fechaPartido,
                    'diaFechaPartido': fechaPartido.split(' ')[0].strip(),
                    'mesFechaPartido': fechaPartido.split(' ')[1].strip(),
                    'anoFechaPartido': fechaPartido.split(' ')[2].strip(),
                    'equipoLocal': equipoLocal,
                    'equipoLocalResultado': equipoLocalResultado,
                    'equipoVisitante': equipoVisitante,
                    'equipoVisitanteResultado': equipoVisitanteResultado,
                    'resultado': str(equipoLocalResultado) + '-' + str(equipoVisitanteResultado)
                })
                partidosConDatos += 1
            else:
                partidosSinDatos += 1

    for equipo,data in dataPosiciones.items():
        data['diferenciaGoles'] = data['golesFavor'] - data['golesEnContra']
        data.update({'torneo': Torneo['nombre']})
        dataSetPosiciones.append(data)
    
    dfposiciones = pd.DataFrame(dataSetPosiciones)
    dfposiciones.to_csv('dataset_posiciones_' + Torneo['nombre'].replace(" ","_") + '.csv', encoding='utf-8')

            
print(f'Partidos con datos: {partidosConDatos}')
print(f'Partidos sin datos: {partidosSinDatos}')
# print(content)

dfpartidos = pd.DataFrame(dataSetPartidos)

#print(dfpartidos.head())

dfpartidos.to_csv('dataset_partidos_torneos_futbol_argentino.csv', encoding='utf-8')