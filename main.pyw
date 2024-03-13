import PySimpleGUI as sg
import cv2
import pyqrcode
import io
from pyzbar import pyzbar

sg.theme('Black')
#password_char='*'
#Debug windows
#sg.Print('Re-routing the stdout', do_not_reroute_stdout=False)

camera = 1
cap = cv2.VideoCapture(camera)

# define the window layout
layout = [
            [sg.Image(filename='', key='-IMAGE-')],
            [sg.Button('Change camera')],
            [sg.InputText(key='-QR-', password_char='*'), sg.Button("Copy"), sg.Button("GenQR")],
]

# create the window and show it without the plot
window = sg.Window('QRcSG', layout, location=(800, 400), icon='qr.ico', element_justification='r')

# ---===--- Event LOOP Read and display frames, operate the GUI --- #

while True:
    try:
        event, values = window.read(timeout=20)

        if event == sg.WIN_CLOSED:
            break

        if event in 'Copy':
            sg.clipboard_set(values['-QR-'])

        if event in 'Change camera':
            camera = 1 if camera == 0 else 0
            cap = cv2.VideoCapture(camera)
            continue

        if event in 'GenQR':
            qr = pyqrcode.create(values['-QR-'], encoding='utf-8')
            buffer = io.BytesIO()
            qr.png(buffer, scale=10)
            sg.Window(values['-QR-'], [[sg.Image(data=buffer.getvalue())], ], icon='qr.ico').read()
        ret, frame = cap.read()                             # Read image from capture device (camera)
        imgbytes=cv2.imencode('.png', frame)[1].tobytes()   # Convert the image to PNG Bytes
        window['-IMAGE-'].update(data=imgbytes)   # Change the Image Element to show the new image
        qr_code = pyzbar.decode(frame)
        if len(qr_code) != 0:
            window['-QR-'].update(qr_code[0].data.decode())
        else:
            continue
    except Exception as ex:
        sg.popup(ex)
        break
window.close()