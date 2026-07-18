import os
import time
import streamlit as st
from groq import Groq

MODEL_NAME = "openai/gpt-oss-20b"

st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>

    /* Campo de texto da API key e caixa de chat com cantos arredondados */
    .stTextInput input, .stChatInput textarea {
        border-radius: 12px !important;
    }

    /* Cartões de mensagem do chat também arredondados */
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
    }

    /* Botões arredondados */
    .stButton button, .stLinkButton a {
        border-radius: 10px !important;
    }

    /* Cor aplicada apenas na palavra "DevMentor" */
    .devmentor-logo {
        font-family: monospace;
        font-weight: 800;
        color: #2563eb;
    }


    /* Faz o espaçador realmente empurrar o que vier depois dele
       para o rodapé da barra lateral */
    .devmentor-spacer {
        flex: 1 1 auto;
    }

    
    </style>
    """,
    unsafe_allow_html=True
)


CUSTOM_PROMPT = """
Você é o "DevMentor AI", um mentor de estudos especialista em Tecnologia da Informação. Sua missão é ajudar pessoas que estão aprendendo TI a entenderem qualquer assunto da área de forma clara, precisa e didática, sempre com foco em aprendizado.

REGRAS DE OPERAÇÃO:
1.  **Foco em TI**: Você pode responder sobre praticamente qualquer assunto de Tecnologia da Informação: programação, algoritmos, estruturas de dados, bancos de dados, redes, cloud computing, DevOps, cibersegurança, inteligência artificial, engenharia de software, sistemas operacionais, ferramentas e frameworks. Se o usuário perguntar sobre algo totalmente fora de TI, responda educadamente que seu foco é mentorar estudos em Tecnologia da Informação.
2.  **Postura de Mentor**: Nunca apenas entregue a resposta pronta sem contexto. Explique o "porquê" das coisas, ajude a pessoa a entender o raciocínio por trás do conceito, e estimule o pensamento crítico e a curiosidade sobre o assunto.
3.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo Prático**: Quando fizer sentido, forneça um ou mais exemplos (código, comandos, diagramas em texto, etc.) bem comentados para ilustrar o conceito.
    * **Detalhamento**: Após o exemplo, descreva em detalhes o que cada parte faz, explicando a lógica envolvida.
    * **Dica de Estudo**: Inclua uma seção chamada "🎯 Dica de Estudo" com uma sugestão prática de como a pessoa pode aprofundar ou praticar esse conhecimento.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da tecnologia em questão.
4.  **Clareza e Precisão**: Use uma linguagem clara, acessível para iniciantes, mas tecnicamente precisa. Evite jargões sem explicá-los.
"""


with st.sidebar:

    st.markdown(
    """
    <div style="margin-top: -50px;">
        <span style="font-size:1.6rem;">🚀</span>
        <span style="font-size:1.3rem; font-weight:700;">
            <span class="devmentor-logo">DevMentor</span> AI
        </span>
    </div>
    """,
    unsafe_allow_html=True
    )

    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )
    if st.button("Salvar Chave", use_container_width=True):
     st.success("Chave salva!")

st.markdown(
"<h2 style='text-align: center;, top'>🚀 <span class='devmentor-logo'>DevMentor</span> AI</h2>",
unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Tire dúvidas sobre qualquer assunto de TI: "
    "programação, redes, nuvem, dados, cibersegurança e muito mais.</p>",
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

if groq_api_key:

    try:
        client = Groq(api_key = groq_api_key)

    except Exception as e:

        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

if prompt := st.chat_input(f"Pergunte algo para o DevMentor"):

    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:

        messages_for_api.append(msg)

    with st.chat_message("assistant"):

        with st.spinner("Pensando na melhor forma de te ensinar isso..."):

            try:

                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = MODEL_NAME,
                    temperature = 0.7,
                    max_tokens = 2048,
                    stream = True,
                )

                def gerador_de_resposta():
                    for chunk in chat_completion:
                        conteudo = chunk.choices[0].delta.content
                        if conteudo:
                            yield conteudo
                            time.sleep(0.03)

                devmentor_resposta = st.write_stream(gerador_de_resposta())
                st.session_state.messages.append({"role": "assistant", "content": devmentor_resposta})
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")