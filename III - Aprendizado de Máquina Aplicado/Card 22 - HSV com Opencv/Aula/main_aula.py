import cv2
import numpy as np

# Carrega a câmera, o 0 e para a webcam principal
cap = cv2.VideoCapture(0)

while True: # Enquanto verdade, enquanto a camera estar aberta
    # Le cada frame da camera
    _, frame = cap.read()
    # Converte o formato de cor do opencv de RGB para HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Cria mascara pra a cor vermelha
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    # coloca a mascara na imagem original
    red = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Faz o mesmo que o vermelho, mas para o azul
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # Agora para a cor verde
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # Agora tudo menos o branco
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # mostra o quadro na janela
    cv2.imshow("Frame", frame)
    # mostra a cor vermelha em vez da mascara
    # cv2.imshow("Red", red)
    # mostra a cor azul em vez da mascara
    # cv2.imshow("Blue", blue)
    # mostra a cor verde em vez da mascara
    # cv2.imshow("Green", green)
    # mostra tudo menos o branco
    cv2.imshow("Result", result)

    # Espera teclar pra sair do loop
    key = cv2.waitKey(1)
    # Se a tecla for o esc
    if key == 27:
        # para o loop
        break