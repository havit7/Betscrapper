#Author: Javier Rodríguez.    .havit7.
import re
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
conexion = sqlite3.connect('apuestas2.db')

cursor = conexion.cursor()

def listar_vivo():

    r = requests.get("https://sports.sportium.es/es/overview", headers={"Content-Type":"text"})

    html = BeautifulSoup(r.text, "html.parser")

    pathequipos = re.compile('<span class="seln-name">(.*?)</span>')

    pathcuotas = re.compile('<span class="price dec">(.*?)</span>')

    pathresults = re.compile('<span class="score">(.*?)</span>')

    z = 0
    x = 0
    r = 0
    for a in html.find_all('div', {'class': 'expander sport-FOOT expander-sport'}):
        equipos = re.findall(pathequipos, str(a))
        cuotas = re.findall(pathcuotas, str(a))
        result = re.findall(pathresults, str(a))
    for z in range(len(equipos)):
        if z % 2 == 0:
            try:
                yep = (equipos[z] + " Vs " + equipos[z+1]).replace(" ", "").replace("-", "").replace(".", "").replace("(", "").replace(")", "").replace("1", "")
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {yep}" \
                        "(Cuota1 REAL, EMPATE REAL, Cuota2 REAL)")
                cursor.execute(f"INSERT INTO {yep}(Cuota1, EMPATE, Cuota2) VALUES(?, ?, ?)", (cuotas[x], cuotas[x+1], cuotas[x+2]))
            except IndexError:
                pass
            r += 1
            x += 3
        z += 2

    conexion.commit()


while True:
    print("Imported!")
    listar_vivo()
    time.sleep(10)
