import os

def format_timestamp(seconds):
    """
    Converte o timestamp de segundos para o formato MM:SS.
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def create_numbered_folder(base_folder="detected_frames"):
    """
    Cria uma nova pasta numerada.
    """
    counter = 1
    while os.path.exists(f"detections/{base_folder}_{counter:02d}"):
        counter += 1
    output_folder = f"detections/{base_folder}_{counter:02d}"
    os.makedirs(output_folder)
    return output_folder
