def should_save_frame(class_id, confidence, last_detections):
    """
    Determina se um frame deve ser salvo com base nas detecções anteriores.
    """
    # Salvar apenas se a confiança for maior ou for uma nova classe
    if class_id not in last_detections or confidence > last_detections[class_id]:
        return True
    return False
