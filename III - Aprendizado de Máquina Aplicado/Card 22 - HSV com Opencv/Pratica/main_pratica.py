import cv2
import numpy as np

# Carrega a câmera, o 0 e para a webcam principal
cap = cv2.VideoCapture(0)
# Para um janela de controla o range de cores
cv2.namedWindow("Controle de Cores")
# Cria as barras de controle para cada range
cv2.createTrackbar("Low H", "Controle de Cores", 0, 179, lambda x: None) # Baixo matiz
cv2.createTrackbar("Low S", "Controle de Cores", 0, 255, lambda x: None) # Baixa saturação
cv2.createTrackbar("Low V", "Controle de Cores", 0, 255, lambda x: None) # Baixo valor
cv2.createTrackbar("High H", "Controle de Cores", 179, 179, lambda x: None) # Alto matiz
cv2.createTrackbar("High S", "Controle de Cores", 255, 255, lambda x: None) # Alta saturação
cv2.createTrackbar("High V", "Controle de Cores", 255, 255, lambda x: None) # Alto valor

while True: # Enquanto verdade, enquanto a camera estar aberta
    # Le cada frame da camera
    _, frame = cap.read()
    # Converte o formato de cor do opencv de RGB para HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Pega os valores das barras de controle
    low_h = cv2.getTrackbarPos("Low H", "Controle de Cores")
    low_s = cv2.getTrackbarPos("Low S", "Controle de Cores")
    low_v = cv2.getTrackbarPos("Low V", "Controle de Cores")
    high_h = cv2.getTrackbarPos("High H", "Controle de Cores")
    high_s = cv2.getTrackbarPos("High S", "Controle de Cores")
    high_v = cv2.getTrackbarPos("High V", "Controle de Cores")

    # Cria uma mask pra filtrar a cor
    low_color = np.array([low_h, low_s, low_v])
    high_color = np.array([high_h, high_s, high_v])
    mask = cv2.inRange(hsv_frame, low_color, high_color)
    # Aplica a mask no frame
    result = cv2.bitwise_and(frame, frame, mask=mask)
    # mostra o quadro na janela
    cv2.imshow("Frame", result)
    # Espera teclar pra sair do loop
    key = cv2.waitKey(1)
    # Se a tecla for o esc
    if key == 27:
        # para o loop
        break

cap.release()
cv2.destroyAllWindows()