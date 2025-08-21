import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Alimento Salvo",
    page_icon=" cibo"
)

# --- FUNÇÃO PARA ENVIAR O E-MAIL (nenhuma mudança aqui) ---
def enviar_email(nome, endereco, telefone, alimentos):
    # Usando o sistema de segredos do Streamlit (st.secrets)
    email_remetente = st.secrets["GMAIL_USER"]
    senha_remetente = st.secrets["GMAIL_PASSWORD"]
    email_destinatario = st.secrets["EMAIL_DESTINATARIO"]

    assunto = f"Nova Doação de Alimentos de: {nome}"
    
    corpo_html = f"""
    <html>
    <body>
        <h2>Nova Notificação de Alimentos para Coleta!</h2>
        <p><strong>Nome do Doador:</strong> {nome}</p>
        <p><strong>Endereço para Coleta:</strong> {endereco}</p>
        <p><strong>Telefone para Contato:</strong> {telefone}</p>
        <hr>
        <h3>Alimentos Disponíveis:</h3>
        <p>{alimentos}</p>
    </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['From'] = email_remetente
    msg['To'] = email_destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo_html, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_remetente, senha_remetente)
        server.sendmail(email_remetente, email_destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# --- INTERFACE DO STREAMLIT ---

st.title("Plataforma de Combate ao Desperdício de Alimentos")
st.write(
    "Tem alimentos sobrando em casa e quer ajudar a combater o desperdício? "
    "Preencha o formulário abaixo que nosso grupo entrará em contato para buscar a doação!"
)

with st.form("formulario_doacao"):
    st.subheader("Informações para Coleta")
    
    nome_pessoa = st.text_input("Seu Nome Completo:")
    
    # --- MUDANÇA 1: SEPARANDO OS CAMPOS DE ENDEREÇO ---
    # Apagamos a linha única de endereço e adicionamos estas.
    
    rua_bairro = st.text_input("Endereço (Rua e Bairro):")
    
    # Usando colunas para deixar a interface mais organizada
    col1, col2 = st.columns(2)
    with col1:
        numero_casa = st.text_input("Número:")
    with col2:
        cidade = st.text_input("Cidade:")

    numero_contato = st.text_input("Seu Telefone/WhatsApp (com DDD):")
    descricao_alimentos = st.text_area("Descreva os alimentos e a quantidade aproximada:")
    
    submitted = st.form_submit_button("Enviar Notificação")

if submitted:
    # --- MUDANÇA 2: JUNTANDO AS INFORMAÇÕES DE ENDEREÇO ---
    # Criamos uma variável que junta os campos de endereço em um texto só.
    
    endereco_completo = f"{rua_bairro}, nº {numero_casa} - {cidade}"
    
    # Verificamos se todos os campos foram preenchidos
    if nome_pessoa and rua_bairro and numero_casa and cidade and numero_contato and descricao_alimentos:
        # Passamos a variável 'endereco_completo' para a função de e-mail
        if enviar_email(nome_pessoa, endereco_completo, numero_contato, descricao_alimentos):
            st.success("Notificação enviada com sucesso! Agradecemos muito a sua colaboração. Em breve entraremos em contato.")
            st.balloons()
        else:
            st.error("Desculpe, ocorreu um erro ao enviar sua notificação. Por favor, tente novamente mais tarde.")
    else:
        st.warning("Por favor, preencha todos os campos antes de enviar.")
