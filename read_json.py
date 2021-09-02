import os
import json
import psycopg2

con = psycopg2.connect(database="colaboraccion", user="postgres", password="sasa", host="127.0.0.1", port="5432")
cur = con.cursor()

rootdir = 'C:/Users/Asus/Desktop/datacrim'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        folderName = path.split('\\')[1]
        fileName = path.split('\\')[2].replace(".json", "")

        f = open(path,)
        data = json.load(f)

        for i in data['features']:
            if "geometry" in i:
                latitud = float(i['geometry']['y'])
                longitud = float(i['geometry']['x'])

                cur.execute("INSERT INTO datacrim.coordenadas(categoria, subcategoria, latitud, longitud) VALUES(%s, %s, %s, %s)",
                (folderName, fileName, latitud, longitud,))
                con.commit()

        f.close()