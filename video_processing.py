import os
import cv2

from detection_logic import should_save_frame


def process_video(video_path, model, output_folder, fps, frame_count, last_detections, detected_frames, timestamps):
    """
    Processa o vídeo, detecta objetos e salva os frames detectados.
    """
    cap = cv2.VideoCapture(video_path)

    # Verificar se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print(f"Erro: Não foi possível abrir o vídeo '{video_path}'.")
        return frame_count, last_detections, detected_frames, timestamps

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break  # Fim do vídeo

        # Calcular timestamp do frame atual
        timestamp = frame_count / fps

        # Rodar inferência do YOLO no frame
        results = model(frame, conf=0.4)

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
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, annotated_frame)
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
