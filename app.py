import os
import cv2

from ultralytics import YOLO

from utils import create_numbered_folder
from video_processing import process_video
from email_sender import send_email_with_pdf
from pdf_generator import create_pdf_with_images


# Configurações do e-mail
EMAIL_SENDER =      "email@gmail.com"    # Seu e-mail
EMAIL_PASSWORD =    "senha"              # Senha do app SMTP
EMAIL_RECEIVER =    "destino@gmail.com"  # Destinatário do e-mail

# Carregar o modelo YOLO treinado
model_trained = YOLO("models\grupo44_v1.pt")

frame_count = 0
last_detections = {}  # Armazena as últimas detecções para evitar repetição
detected_frames = []  # Lista para armazenar os frames detectados
timestamps = []       # Lista para armazenar os timestamps dos frames detectados

# Abrir o vídeo
video_path = "videos/video2.mp4"

# Criar diretório para salvar os frames detectados
output_folder = create_numbered_folder()

# Obter FPS do vídeo para calcular tempo
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.release()

# Processar os frames do vídeo
frame_count, last_detections, detected_frames, timestamps = process_video(
    video_path, model_trained, output_folder, fps, frame_count, last_detections, detected_frames, timestamps
)

# Criar e enviar o relatório PDF ao final do vídeo
if detected_frames:
    pdf_filename = os.path.join(output_folder, "relatorio_detectado.pdf")
    create_pdf_with_images(detected_frames, timestamps, pdf_filename)
    send_email_with_pdf(pdf_filename, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER)
else:
    print("Nenhum objeto detectado. PDF não gerado.")
