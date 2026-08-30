import psycopg


def consulta(latitude, longitude, raio_km):
    raio_metros = raio_km * 1000

    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="cep_geofinder",
        user="postgres",
        password="SUA_SENHA"
    )

    cursor = connection.cursor()

    cursor.execute("""
            SELECT cep, latitude, longitude
            FROM ceps
            WHERE location IS NOT NULL
              AND ST_DWithin(
                  location::geography,
                  ST_SetSRID(
                      ST_MakePoint(%s, %s),
                      4326
                  )::geography,
                  %s
              )
            ORDER BY ST_Distance(
                location::geography,
                ST_SetSRID(
                    ST_MakePoint(%s, %s),
                    4326
                )::geography
            );
        """, (
        longitude,
        latitude,
        raio_metros,
        longitude,
        latitude
    ))

    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
