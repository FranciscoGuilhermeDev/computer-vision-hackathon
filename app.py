import os
import cv2
import streamlit as st

import config

from ultralytics import YOLO

from utils import create_numbered_folder
from video_processing import run_detection_pipeline
from email_sender import send_email_with_pdf
from pdf_generator import create_pdf_with_images


# 📌 Carregar modelo YOLO uma única vez
@st.cache_resource
def load_model():
    return YOLO(config.MODEL_PATH)

model_trained = load_model()

# 📌 Interface do Streamlit
st.title("🔪 Detecção de Objetos Cortantes em Vídeo")

# Upload do vídeo pelo usuário
uploaded_file = st.file_uploader("Carregue um vídeo", type=["mp4", "avi"])

# Verifica se um vídeo foi carregado
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
        # Opção para enviar e-mail (antes do processamento)
        send_email = st.checkbox("📩 Enviar e-mail após processamento?")

        # Botão para iniciar o processamento
        if st.button("🔍 CLIQUE AQUI para iniciar Processamento"):
            with st.spinner("⏳ Processando vídeo... Isso pode levar alguns minutos."):

                # Criar diretório para salvar os frames detectados
                output_folder = create_numbered_folder(config.OUTPUT_FOLDER_BASE)

                # Obter FPS do vídeo para calcular tempo
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                cap.release()

                # Placeholder para atualizar a interface dinamicamente
                status_text = st.empty()
                status_text.text("🔄 Analisando frames do vídeo...")

                # Processar os frames do vídeo
                detected_frames, timestamps = run_detection_pipeline(
                    video_path, model_trained, output_folder, fps
                )

                # Criar e enviar o relatório PDF ao final do vídeo
                if detected_frames:
                    pdf_filename = os.path.join(output_folder, "relatorio_detectado.pdf")
                    create_pdf_with_images(detected_frames, timestamps, pdf_filename)
                    
                    # Enviar e-mail somente se o checkbox foi marcado ANTES
                    if send_email:
                        send_email_with_pdf(pdf_filename, config.EMAIL_SENDER, config.EMAIL_PASSWORD, config.EMAIL_RECEIVER)
                    
                    st.success("✅ Processamento concluído com sucesso!")
                else:
                    st.error("⚠ Nenhum objeto detectado. PDF não gerado.")
                # Remover o status de processamento
                status_text.empty()
else:
    st.info("📂 Por favor, carregue um arquivo de vídeo para iniciar o processamento.")
