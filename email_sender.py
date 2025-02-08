import os
import smtplib

from email.message import EmailMessage


def send_email_with_pdf(pdf_path, email_sender, email_password, email_receiver):
    """
    Envia um único e-mail contendo o relatório PDF como anexo.

    Args:
        pdf_path (str): O caminho para o arquivo PDF a ser anexado.
        email_sender (str): O endereço de e-mail do remetente.
        email_password (str): A senha do e-mail do remetente.
        email_receiver (str): O endereço de e-mail do destinatário.

    Returns:
        None
    """
    msg = EmailMessage()
    msg["Subject"] = "Relatório de Detecção YOLO"
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg.set_content("Segue o relatório de detecção em anexo.")

    # Anexar o PDF ao e-mail
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

    # Enviar o e-mail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_sender, email_password)
            server.send_message(msg)
        print(f"E-mail enviado com o relatório: {pdf_path}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
