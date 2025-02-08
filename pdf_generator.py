from fpdf import FPDF
from utils import format_timestamp


def create_pdf_with_images(image_paths, timestamps, pdf_filename):
    """
    Cria um PDF com imagens e timestamps.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=10)

    images_per_page = 8      # 2 colunas x 4 linhas
    img_w, img_h = 95, 50    # Tamanho das imagens no PDF
    x_positions = [10, 110]  # Posições X para 2 colunas
    y_positions = [20, 80, 140, 200]  # Posições Y para 4 linhas

    for i, img_path in enumerate(image_paths):
        if i % images_per_page == 0:  # Nova página a cada 8 imagens
            pdf.add_page()
            pdf.cell(200, 10, "Relatório de Detecção YOLO", ln=True, align='C')
            pdf.ln(5)

        # Coordenadas para posicionar a imagem
        x = x_positions[(i % images_per_page) % 2]  # Alterna entre 2 colunas
        y = y_positions[(i // 2) % 4] # Alterna entre 4 linhas (dividindo por 2 para 4 colunas)

        # Adicionar a imagem
        pdf.image(img_path, x=x, y=y, w=img_w, h=img_h)

        # Adicionar o timestamp formatado abaixo da imagem
        timestamp_text = f"Tempo: {format_timestamp(timestamps[i])}"
        pdf.text(x, y + img_h + 5, timestamp_text)

    pdf.output(pdf_filename)
    print(f"Relatório PDF gerado: {pdf_filename}")
