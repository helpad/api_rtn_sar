import csv
from datetime import datetime

import PySimpleGUI as sg

from sar_service import SarService

# Definir la interfaz de usuario
layout = [
    [sg.Text('Archivo CSV'), sg.InputText(), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Button('Cargar CSV'), sg.Button('Obtener información')],
    [sg.Table(values=[], headings=['documento'], key='-documentos-', enable_events=True),
     sg.Table(values=[], headings=['nombre', 'rtn', 'identificacion'], key='-info-',
              enable_events=True)],
    [sg.Radio('rtn', group_id='documento', default=True, key='-rtn-'),
     sg.Radio('dni', group_id='documento', key='-dni-')],
    [sg.Button('Exportar')],
]

# Crear la ventana GUI
window = sg.Window('RTN SAR', layout)

tabla_documentos = []
tabla_info = []
sar_service = SarService('https://enlacertn.sar.gob.hn/index.aspx')

# Event loop para procesar eventos y obtener entrada del usuario
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    # Manejar el evento del botón 'Cargar CSV'
    if event == 'Cargar CSV':
        csv_file_path = values[0]
        tabla_documentos = []
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Omitir la fila de encabezado
            for row in csv_reader:
                tabla_documentos.append(row)
        window['-documentos-'].update(values=tabla_documentos)

    # Manejar el evento del botón 'Obtener información'
    if event == 'Obtener información':
        tipo_documento = 'RTN' if values['-rtn-'] else 'DNI'
        tabla_info = []
        for row in tabla_documentos:
            try:
                info = sar_service.get_sar_info(tipo_documento, row[0])
                tabla_info.append([info.nombre, info.rtn, info.identificacion, ])
            except ValueError:
                tabla_info.append([
                    'N/A',
                    row[0] if tipo_documento == 'RTN' else 'N/A',
                    row[0] if tipo_documento == 'DNI' else 'N/A',
                ])
        window['-info-'].update(values=tabla_info)

    # Manejar el evento del botón 'Exportar'
    if event == 'Exportar':
        csv_file_path = f'datos_sar_{datetime.now().date()}.csv'
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['nombre', 'rtn', 'identificacion'])
            for row in tabla_info:
                csv_writer.writerow(row)
