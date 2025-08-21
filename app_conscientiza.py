import streamlit as st
import smtplib
import pandas as pd
import pydeck as pdk  # <-- AQUI ESTÁ A CORREÇÃO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Alimento Salvo - Ipiranga/PI",
    page_icon="🌱",
    layout="wide"
)

# --- FUNÇÃO PARA ENVIAR O E-MAIL (Sua função original) ---
def enviar_email(nome, endereco, telefone, alimentos):
    try:
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

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_remetente, senha_remetente)
        server.sendmail(email_remetente, email_destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        # No ambiente de produção, é melhor logar o erro em vez de printar
        st.error(f"Erro ao configurar o serviço de e-mail: {e}")
        return False

# --- HEADER ---
# Substitua "seu_logo.png" pelo nome do seu arquivo de imagem
try:
    st.image("logo.png", width=150)
except:
    st.write(" ") # Espaço reservado caso não encontre o logo

st.title("Plataforma Alimento Salvo")
st.subheader("Conectando quem tem de sobra com quem precisa em Ipiranga do Piauí.")
st.markdown("---")


# --- ESTRUTURA COM ABAS ---
tab_doar, tab_impacto, tab_info = st.tabs([
    "📝 QUERO DOAR!", 
    "📈 NOSSO IMPACTO E ATUAÇÃO", 
    "ℹ️ COMO FUNCIONA & DÚVIDAS"
])


# --- ABA 1: FORMULÁRIO DE DOAÇÃO ---
with tab_doar:
    st.header("Preencha para agendarmos a coleta")
    
    with st.form("formulario_doacao"):
        st.subheader("Informações para Coleta")
        
        nome_pessoa = st.text_input("Seu Nome Completo:")
        
        rua = st.text_input("Rua/Avenida:")
        bairro = st.text_input("Bairro:")
        
        col1, col2 = st.columns(2)
        with col1:
            numero_casa = st.text_input("Número:")
        with col2:
            cidade = st.text_input("Cidade:", value="Ipiranga do Piauí", disabled=True)

        numero_contato = st.text_input("Seu Telefone/WhatsApp (com DDD):")
        descricao_alimentos = st.text_area("Descreva os alimentos e a quantidade aproximada:")
        
        submitted = st.form_submit_button("Enviar Notificação de Doação")

    if submitted:
        endereco_completo = f"{rua}, nº {numero_casa}, Bairro {bairro} - {cidade}"
        
        if nome_pessoa and rua and bairro and numero_casa and numero_contato and descricao_alimentos:
            if enviar_email(nome_pessoa, endereco_completo, numero_contato, descricao_alimentos):
                st.success("Notificação enviada com sucesso! Agradecemos muito a sua colaboração. Em breve entraremos em contato.")
                st.balloons()
                st.markdown("---")
                st.write("#### Ajude-nos a ir mais longe!")
                st.write("Compartilhe nosso projeto com seus amigos e familiares. Juntos, podemos combater ainda mais o desperdício.")
                # Link de compartilhamento para WhatsApp
                st.link_button("Compartilhar no WhatsApp", "https://wa.me/?text=Estou%20ajudando%20a%20combater%20o%20desperdício%20de%20alimentos%20com%20o%20projeto%20Alimento%20Salvo%20em%20Ipiranga/PI!%20Conheça%20você%20também:%20combateaodesperdicioipi.streamlit.app")
            else:
                st.error("Desculpe, ocorreu um erro ao enviar sua notificação. Verifique se suas credenciais de e-mail estão configuradas corretamente ou tente novamente mais tarde.")
        else:
            st.warning("Por favor, preencha todos os campos antes de enviar.")


# --- ABA 2: CALCULADORA DE IMPACTO E MAPA ---
with tab_impacto:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("Calcule o Impacto da Sua Doação!")
        
        refeicoes_por_item = {
            "Arroz, Feijão ou Macarrão (Kg)": 4,
            "Pães (unidade)": 2,
            "Frutas e Legumes (Kg)": 3,
            "Leite (Litro)": 4
        }
        alimento_selecionado = st.selectbox(
            "Qual o principal alimento que você vai doar?",
            options=list(refeicoes_por_item.keys())
        )
        quantidade = st.number_input("Qual a quantidade?", min_value=0.5, step=0.5)

        if st.button("Calcular Impacto"):
            total_refeicoes = refeicoes_por_item[alimento_selecionado] * quantidade
            st.success(f"🎉 Sua doação pode gerar aproximadamente **{int(total_refeicoes)} refeições!**")

    with col2:
        st.header("Nossa Área de Atuação")
        st.success("Atendemos em **toda zona urbana de Ipiranga do Piauí!**")
        st.write("O círculo no mapa representa nossa área de coleta.")
        
        # CÓDIGO DO MAPA ATUALIZADO
        lat_ipiranga = -6.8225
        lon_ipiranga = -41.7328

        view_state = pdk.ViewState(
            latitude=lat_ipiranga,
            longitude=lon_ipiranga,
            zoom=13,
            pitch=50,
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame({'lat': [lat_ipiranga], 'lon': [lon_ipiranga]}),
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=4000,
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# --- ABA 3: INFORMAÇÕES E DÚVIDAS ---
with tab_info:
    st.header("Como sua doação funciona na prática")
    st.markdown("""
    1.  **📝 Preenchimento do Formulário:** Você nos informa os detalhes da doação aqui no site.
    2.  **📱 Contato via WhatsApp:** Nossa equipe entrará em contato no número informado para confirmar os itens e agendar o melhor horário para a coleta.
    3.  **🚚 Coleta Segura:** Um de nossos voluntários irá até o endereço para retirar a doação.
    4.  **❤️ Entrega ao Destino:** Os alimentos são imediatamente direcionados para famílias e instituições parceiras em nossa comunidade.
    """)
    st.markdown("---")
    
    st.header("Dúvidas Frequentes")
    with st.expander("❓ Que tipo de alimento posso doar?"):
        st.write("Aceitamos alimentos não perecíveis (arroz, feijão, macarrão, etc.) e também alimentos frescos (frutas, legumes, pães), desde que estejam em bom estado para consumo.")

    with st.expander("❓ Em quanto tempo vocês entram em contato?"):
        st.write("Geralmente, nosso contato é feito em até 24 horas úteis após o envio do formulário.")

    with st.expander("❓ Há algum custo para a coleta?"):
        st.write("Não! Nosso serviço é totalmente voluntário e gratuito, focado em ajudar a comunidade.")
