from influxdb import InfluxDBClient
from datetime import datetime
from secret import *
import settings
import glob

client = InfluxDBClient(db_host, db_port, db_user, db_password, db_database)


def define_json(measurement, time, fields):
    #fields es un diccionario {"value": 0.64}
    # time es datetime
    # measurement es lo que se está midiendo
    json_body = [
        {
            "measurement": [measurement],
            "tags": {
                "provider": "KC-BD-FF",
            },
            "time": time.isoformat(),
            "fields": fields

        }
    ]
    return json_body


def archivos_para_procesar():
    directorio = settings.SCRAP_DIR + '*'
    lista_archivos = glob.glob(directorio)
    return len(lista_archivos)

def main():
    ahora = datetime.now()
    fields = {"value": archivos_para_procesar()}
    #fields = {"value":10}
    json_body = define_json('Archivos en scrap',ahora, fields)
    print(json_body)
    client.write_points(json_body)
    pass

if __name__ == '__main__':
    main()
