from influxdb import InfluxDBClient
from datetime import datetime
from secret import *
import settings
import glob
import logging

client = InfluxDBClient(db_host, db_port, db_user, db_password, db_database)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


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


def archivos_procesados():
    directorio = settings.PROCESS_DIR + '*'
    lista_archivos = glob.glob(directorio)
    return len(lista_archivos)


def main():
    monitoring_logger = setup_logger('monitoring_log', 'monitoring.log')

    ahora = datetime.now()


    # Archivos para procesar
    files_to_process = archivos_para_procesar()
    fields = {"value": files_to_process}
    json_body = define_json('Archivos en scrap',ahora, fields)
    client.write_points(json_body)

    # Archivos procesados
    files_processed = archivos_procesados()
    fields = {"value": archivos_procesados()}
    json_body = define_json('Archivos procesados', ahora, fields)
    client.write_points(json_body)

    # registros en tablas


    # logging
    mensaje = f"Enviado a influx a las {ahora}, archivos para procesar: {files_to_process}, " \
              f"archivos procesados: {files_processed}"

    monitoring_logger.info(mensaje)
    #



if __name__ == '__main__':
    main()
