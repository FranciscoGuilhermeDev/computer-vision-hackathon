import cv2
import config
import logging

from detection_logic import should_save_frame


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_detection_pipeline(video_path, model, output_folder, fps):
    frame_count, last_detections = 0, {}
    detected_frames, timestamps = [], []

    frame_count, last_detections, detected_frames, timestamps = process_video(
        video_path, model, output_folder, fps, frame_count, last_detections, detected_frames, timestamps
    )

    return detected_frames, timestamps


def process_video(video_path, model, output_folder, fps, frame_count, last_detections, detected_frames, timestamps):
    """
    Processa o vídeo, detecta objetos e salva os frames detectados.

    Args:
        video_path (str): O caminho para o arquivo de vídeo.
        model: O modelo YOLO para detecção de objetos.
        output_folder (str): O caminho para a pasta onde os frames detectados serão salvos.
        fps (float): A taxa de quadros do vídeo.
        frame_count (int): O número de frames processados até o momento.
        last_detections (dict): Um dicionário contendo as últimas detecções de objetos.
        detected_frames (list): Uma lista contendo os caminhos dos frames detectados.
        timestamps (list): Uma lista contendo os timestamps dos frames detectados.

    Returns:
        tuple: Uma tupla contendo:
            - frame_count (int): O número total de frames processados.
            - last_detections (dict): As últimas detecções de objetos.
            - detected_frames (list): A lista de caminhos dos frames detectados.
            - timestamps (list): A lista de timestamps dos frames detectados.
    """
    logging.info(f"Iniciando processamento do vídeo {video_path}")
    cap = cv2.VideoCapture(video_path)

    # Verificar se o vídeo foi aberto corretamente
    if not cap.isOpened():
        logging.error(f"Erro ao abrir vídeo: {video_path}")
        print(f"Erro: Não foi possível abrir o vídeo '{video_path}'.")
        return frame_count, last_detections, detected_frames, timestamps

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break  # Fim do vídeo

        # Calcular timestamp do frame atual
        timestamp = frame_count / fps

        # Rodar inferência do YOLO no frame
        results = list(model(frame, conf=config.CONFIDENCE_THRESHOLD)) # Converter o gerador para uma lista

        # Gerar a imagem com as caixas desenhadas
        annotated_frame = results[0].plot()

        # Guardar as detecções do frame atual
        current_detections = {}

        for box in results[0].boxes:
            class_id = int(box.cls[0])       # ID da classe detectada
            confidence = float(box.conf[0])  # Confiança da detecção

            # Salvar apenas se a confiança for maior ou for uma nova classe
            if should_save_frame(class_id, confidence, last_detections):
                current_detections[class_id] = confidence

        # Se houve mudanças nas detecções, salvar o frame e adicioná-lo à lista
        if current_detections:
            frame_filename = f"{output_folder}/frame_{frame_count}.jpg"
            cv2.imwrite(frame_filename, annotated_frame)
            logging.info(f"Frame salvo: {frame_filename}")
            print(f"Frame salvo: {frame_filename}")

            # Adicionar o frame salvo e seu timestamp às listas
            detected_frames.append(frame_filename)
            timestamps.append(timestamp)

        # Atualizar as últimas detecções
        last_detections = current_detections.copy()

        # # Exibir a imagem anotada
        # cv2.imshow("YOLO Inference", annotated_frame)

        # # Pressionar 'q' para sair
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break

        frame_count += 1

    # Fechar vídeo e janelas
    cap.release()
    cv2.destroyAllWindows()

    return frame_count, last_detections, detected_frames, timestamps
