def should_save_frame(class_id, confidence, last_detections):
    """
    Determina se um frame deve ser salvo com base nas detecções anteriores.

    Args:
        class_id (int): O ID da classe detectada.
        confidence (float): A confiança da detecção.
        last_detections (dict): Um dicionário contendo as últimas detecções por classe.

    Returns:
        bool: True se o frame deve ser salvo, False caso contrário.
    """
    # Salvar apenas se a confiança for maior ou for uma nova classe
    if class_id not in last_detections or confidence > last_detections[class_id]:
        return True
    return False
