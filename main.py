import PySimpleGUI as sg
import cv2
import pyqrcode


sg.theme('Black')

# define the window layout
layout = [
            [sg.Image(filename='', key='-IMAGE-', tooltip='Right click for exit menu')],
            [sg.Button('Exit')],
            [sg.InputText(key='-QR-'), sg.Button("GenQR")],

]

# create the window and show it without the plot
window = sg.Window('Demo Application - OpenCV Integration', layout, location=(800,400),
                   right_click_menu=['Right', ['Exit'], ], )

# ---===--- Event LOOP Read and display frames, operate the GUI --- #
cap = cv2.VideoCapture(1)                               # Setup the OpenCV capture device (webcam)
detector = cv2.QRCodeDetector()
while True:
    event, values = window.read(timeout=20)
    if event in ('Exit', None):
        break

    if event in ('GenQR'):
        qr = pyqrcode.create(window['-QR-'])
        sg.popup(image=qr.png())
    ret, frame = cap.read()                             # Read image from capture device (camera)
    imgbytes=cv2.imencode('.png', frame)[1].tobytes()   # Convert the image to PNG Bytes
    window['-IMAGE-'].update(data=imgbytes)   # Change the Image Element to show the new image
    data, points, _ = detector.detectAndDecode(frame)

    if points is not None:
        window['-QR-'].update(data)

    else:
        continue

window.close()