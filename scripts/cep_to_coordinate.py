import psycopg
import requests
import time

def geocode():
    url = "http://127.0.0.1:8088/search"
    #cont = 0
    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="cep_geofinder",
        user="postgres",
        password="SUA_SENHA"
    )
    cursor = connection.cursor()
    update_cursor = connection.cursor()
    cursor.execute("""
        SELECT cep, logradouro, cidade, uf
        FROM ceps
        WHERE latitude IS NULL
            AND longitude IS NULL
    """)

    for row in cursor:
        time.sleep(1)
        cep = row[0]

        parameters = { "postalcode": cep, "country": "Brazil", "format": "jsonv2", "limit": 1 }

        headers = {
            "User-Agent": "cep-geofinder/1.0"
        }
        response = requests.get(
            url,
            params=parameters,
            headers=headers
        )
        response.raise_for_status()

        data = response.json()
        print("CEP:", cep)
        print("Resultado:", data)
        if not data:
            lat = None
            lon = None
        else:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            update_cursor.execute("""
                           UPDATE ceps
                           SET latitude = %s,
                               longitude = %s
                           WHERE cep = %s;
                                  """, (lat, lon, cep))

        #Exists for debug purposes:
        #cont+=1 Debug option
        #if cont >= 5:
        #    break

    connection.commit()

    update_cursor.close()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    geocode()