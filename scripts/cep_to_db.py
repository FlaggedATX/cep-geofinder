import psycopg
import os
import json

opencep_path = "../data/opencepdata/v1/" #Insert here the path to your OpenCEP dataset folder

def opencep_to_db(opencep_path):

    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="cep_geofinder",
        user="postgres",
        password="SUA_SENHA"
    )
    cursor = connection.cursor()

    for file in os.listdir(opencep_path):
        print("opencep_path: ", file)
        with open(opencep_path + file, 'r', encoding="utf-8") as f:
            data = json.load(f)

        cep = data["cep"]
        cep = cep.replace("-", "")
        logradouro = data["logradouro"]
        neighborhood = data["bairro"]
        city = data["localidade"]
        uf = data["uf"]

        if uf == "SP" and city == "São Paulo":
            cursor.execute("""
                           INSERT INTO ceps (cep,
                                             logradouro,
                                             bairro,
                                             cidade,
                                             uf)
                           VALUES (%s, %s, %s, %s, %s) ON CONFLICT (cep) DO NOTHING;
                           """, (cep, logradouro, neighborhood, city, uf))


    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    opencep_to_db(opencep_path)

