# 🔪 Detecção de Objetos Cortantes em Vídeos com YOLOv11

Este projeto utiliza Python, Streamlit e YOLOv11 para detectar objetos cortantes em vídeos, gerar relatórios em PDF e, opcionalmente, enviá-los por e-mail.

## Funcionalidades

- Upload de vídeos para análise.
- Detecção de objetos cortantes com YOLOv11.
- Geração automática de um relatório em PDF com imagens detectadas.
- Envio opcional por e-mail do relatório gerado.

## 1. Como Instalar e Executar o Projeto

### 1.1 Clonar o Repositório

Abra o terminal e execute:

```shell
git clone https://github.com/FranciscoGuilhermeDev/computer-vision-hackathon.git
cd computer-vision-hackathon
```

### 1.2 Criar e Ativar um Ambiente Virtual (Recomendado)

Windows (cmd ou PowerShell):

```shell
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```shell
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Instalar as Dependências

```shell
pip install -r requirements.txt
```

### 1.4 Executar o Streamlit

```shell
streamlit run app.py
```

- O aplicativo será aberto automaticamente no navegador.
- O indicado é o Microsoft Edge, por permitir abrir arquivos localmente

## 2. Configuração do Envio de E-mail

No arquivo `config.py`, configure o e-mail:

EMAIL_SENDER = "seu_email@gmail.com"<br>
EMAIL_PASSWORD = "sua_senha_de_app"<br>
EMAIL_RECEIVER = "destinatario@gmail.com"<br>

⚠ Importante: Se usar Gmail, ative "Senhas de App" para permitir o envio automático.

## 3. Estrutura do Projeto

SEU_REPOSITORIO/<br>
│── models/ -------------------- # Pasta do modelo YOLO<br>
│   ├── grupo44_v1.pt ----------- # Modelo treinado<br>
│── detections/ ----------------- # Pasta para frames detectados<br>
│── app.py ----------------------  # Interface Streamlit<br>
│── config.py ------------------- # Configurações do projeto<br>
│── video_processing.py ------- # Processamento de vídeo<br>
│── detection_logic.py --------- # Lógica de detecção<br>
│── email_sender.py ----------- # Envio de e-mail<br>
│── pdf_generator.py ---------- # Geração do relatório PDF<br>
│── utils.py --------------------- # Funções utilitárias<br>
│── requirements.txt ----------- # Pacotes necessários<br>
│── README.md ----- --------- # Documentação do projeto<br>

## 4. Próximos Passos

- Melhorar a interface do usuário no Streamlit.
- Adicionar suporte para múltiplos modelos de detecção.
- Otimizar a performance da inferência.

## 5. Contribuindo

Fique à vontade para abrir Issues ou enviar Pull Requests!

Se precisar de ajuda, entre em contato.
