import os
import cv2
import streamlit as st

from ultralytics import YOLO

from utils import create_numbered_folder
from video_processing import process_video
from email_sender import send_email_with_pdf
from pdf_generator import create_pdf_with_images


# Configurações do e-mail
EMAIL_SENDER =      "email@gmail.com"    # Seu e-mail
EMAIL_PASSWORD =    "senha"              # Senha do app SMTP
EMAIL_RECEIVER =    "destino@gmail.com"  # Destinatário do e-mail

frame_count = 0
last_detections = {}  # Armazena as últimas detecções para evitar repetição
detected_frames = []  # Lista para armazenar os frames detectados
timestamps = []       # Lista para armazenar os timestamps dos frames detectados

# Interface do Streamlit
st.title("Detecção de Objetos Cortantes em Vídeo")

# Upload do vídeo pelo usuário
uploaded_file = st.file_uploader("Carregue um vídeo", type=["mp4", "avi"])

if uploaded_file:
    # Salvar o arquivo temporariamente
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    # Criar layout com duas colunas
    col1, col2 = st.columns([3, 1])  # 75% vídeo, 25% botão

    with col1:
        st.video(video_path)

    with col2:
        # Botão para iniciar o processamento
        if st.button("🔍 CLIQUE AQUI para iniciar Processamento"):
            with st.spinner("⏳ Processando vídeo... Isso pode levar alguns minutos."):
                # Carregar o modelo YOLO treinado
                model_trained = YOLO("models/grupo44_v1.pt")

                # Criar diretório para salvar os frames detectados
                output_folder = create_numbered_folder()

                # Obter FPS do vídeo para calcular tempo
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                cap.release()

                # Placeholder para atualizar a interface dinamicamente
                status_text = st.empty()
                status_text.text("Processando frames do vídeo...")

                # Processar os frames do vídeo
                frame_count, last_detections, detected_frames, timestamps = process_video(
                    video_path, model_trained, output_folder, fps, frame_count, last_detections, detected_frames, timestamps
                )

                # Criar e enviar o relatório PDF ao final do vídeo
                if detected_frames:
                    pdf_filename = os.path.join(output_folder, "relatorio_detectado.pdf")
                    status_text.text("Gerando relatório PDF...")
                    create_pdf_with_images(detected_frames, timestamps, pdf_filename)
                    send_email_with_pdf(pdf_filename, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER)
                    st.success("✅ Processamento concluído com sucesso!")
                else:
                    st.error("⚠ Nenhum objeto detectado. PDF não gerado.")
                # Remover o status de processamento
                status_text.empty()
else:
    st.info("📂 Por favor, carregue um arquivo de vídeo para iniciar o processamento.")
