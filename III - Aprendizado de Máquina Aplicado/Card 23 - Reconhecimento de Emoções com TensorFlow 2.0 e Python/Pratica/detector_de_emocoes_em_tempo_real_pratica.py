import cv2
import numpy as np
from tensorflow.keras.models import load_model

ARQUIVO_MODELO = "modelo_07_expressoes_dataaug.keras" # modelo treinado
ARQUIVO_CASCADE = "haarcascade_frontalface_default_pratica.xml"

# classes de expressões faciais que o modelo foi treinado para reconhecer
EXPRESSOES = ["Raiva", "Nojo", "Medo", "Feliz", "Triste", "Surpreso", "Neutro"]

# carrega o modelo e o detector de faces
modelo = load_model(ARQUIVO_MODELO, compile=False)
face_detector = cv2.CascadeClassifier(ARQUIVO_CASCADE)

def prever_emocao(face_cinza):
    # mesmo pre-processamento usado no treinamento: 48x48, 1 canal, normalizado 0-1
    roi = cv2.resize(face_cinza, (48, 48))
    roi = roi.astype("float32") / 255.0
    roi = np.expand_dims(np.expand_dims(roi, -1), 0)  # vira (1, 48, 48, 1)
    predicao = modelo.predict(roi, verbose=0)[0]
    indice = int(np.argmax(predicao))
    return EXPRESSOES[indice], predicao[indice]

# loop principal
# pega frame, detecta rosto(s), prediz emocao, desenha na tela
captura = cv2.VideoCapture(0)

if not captura.isOpened():
    # se nao conseguir abrir a camera, levanta um erro
    raise RuntimeError("Nao consegui abrir a camera. Confere o id da camera.")

while True:
    ok, frame = captura.read()
    if not ok:
        break

    # converte para escala de cinza e detecta faces
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(cinza, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    # para cada face detectada, prediz a emoção e desenha retângulo e texto na tela
    for (x, y, w, h) in faces:
        roi_cinza = cinza[y:y + h, x:x + w]
        emocao, confianca = prever_emocao(roi_cinza)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, emocao, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f"{confianca * 100:.0f}%", (x, y + h + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow("Deteccao de emocoes - aperte q pra sair", frame)
    # se a tecla 'q' for pressionada, sai do loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

captura.release()
cv2.destroyAllWindows()