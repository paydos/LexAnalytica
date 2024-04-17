import streamlit as st

from utils.acknowledge import show_creator_acknowledgement
from utils.pwd import check_password

st.set_page_config(
    page_title="LexAnalytica",
    page_icon="data/branded_icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)


col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 3, 2])
L, R = st.columns(2, gap="medium")

with col2:
    st.title(
        "About 📘",
    )

with L:
    st.subheader("Configuración y Uso de LexAnalytica")
    st.markdown(
        """
        Para explicar cómo se ha configurado y utilizado la IA LexAnalytica para responder a preguntas de tests de acceso a la abogacía, describiré los distintos componentes y decisiones tomadas en el proceso.
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Uso de la Vector Store y ajuste de parámetros:")
    st.markdown(
        """
        - **Vector Store**: Para garantizar la máxima precisión y relevancia de los datos, se ha procedido a la carga del Vector Store con legislación y material doctrinal de suma importancia, optando deliberadamente por una operación desconectada de la red global de Internet. Esta decisión se fundamenta en la exploración exhaustiva de las posibilidades que ofrece el acceso a Internet, concluyendo que su uso podría comprometer la integridad y especificidad de la información al introducir potenciales errores derivados de fuentes no verificadas.
        - **Temperatura de generación**: La configuración de la temperatura de generación se ha establecido en 0.15, con el objetivo de restringir la variabilidad en las respuestas generadas por el sistema y minimizar la generación de contenido no basado en datos fiables. Esta medida refuerza la determinación y precisión de las respuestas, elementos críticos en el ámbito jurídico, donde la exactitud y la fiabilidad son imperativas.
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Protocolos de Elaboración de Respuestas:")
    st.markdown(
        """
        Hemos implementado un conjunto de protocolos meticulosamente definidos para la elaboración de respuestas. Estos protocolos permiten al sistema realizar un análisis lógico y fundamentado para determinar la veracidad de cada opción presentada en los tests, basándose en pilares jurídicos robustos como la legislación vigente, la jurisprudencia relevante y la doctrina establecida.
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Configuración Avanzada del FusionRAG:")
    st.markdown(
        """
        - **Parámetros de Búsqueda**: Optamos por una configuración de 5x5 en el FusionRAG, aprovechando al máximo el límite permitido. Esta configuración estratégica posibilita la exploración exhaustiva de la información disponible para cada consulta, garantizando una cobertura integral y minuciosa de las cuestiones jurídicas pertinentes.
        - **Contextualización de Consultas**: La preparación del contexto para las interacciones con el FusionRAG se ha diseñado meticulosamente para convertir las interrogantes de los usuarios en consultas especializadas que maximicen la eficacia de la búsqueda en la Vector Store. Esto se logra mediante la identificación precisa de los temas clave, basándose en la categoría jurídica correspondiente y la formulación de consultas de búsqueda altamente específicas.
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Estructuración y Redacción del Prompt para GPT-4:")
    st.markdown(
        """
        La estructura y redacción del prompt se han cuidadosamente elaborado para dirigir al modelo de inteligencia artificial GPT-4 hacia la generación de respuestas que no solo determinen la opción correcta, sino que también proporcionen una justificación exhaustiva de esta elección, respaldada por referencias específicas a legislación, jurisprudencia y doctrina.
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        En resumen, estamos convencidos de que este enfoque meticuloso asegura que el agente de inteligencia artificial ofrezca respuestas bien fundamentadas y precisas, reflejando una comprensión profunda de las materias legales pertinentes y las competencias analíticas esenciales para el ejercicio de la abogacía. Cada componente ha sido cuidadosamente ajustado para optimizar la exactitud y pertinencia de las respuestas en el marco del Examen de Acceso a la Abogacía.
    """,
        unsafe_allow_html=True,
    )
with col5:
    st.title("Arquitectura 🛠️")

with R:
    with st.expander("📐 Diagrama de Arquitectura"):
        st.image("data/archHackathon.png")
    with st.expander("# 🛠️ Tech Stack"):
        st.markdown(
            """
    - **Lenguaje de Programación:** Python 🐍
    - **Interfaz de Usuario:** Streamlit
    - **Modelos de Lenguaje:** OpenAI
    - **Gestión de Embeddings:** Pinecone
    - **Framework de Desarrollo:** LangChain 🦜
    """
        )

    st.subheader("Backend")
    st.write(
        """
        La arquitectura de backend de nuestro sistema se fundamenta completamente en Python, con un enfoque full-stack para el desarrollo de LexAnalytica. Inicialmente, valoramos la implementación de un modelo de Hugging Face open-source; sin embargo, las restricciones inherentes a la infraestructura de este servidor nos llevaron a optar por la plataforma OpenAI ya que nos ofrecen una base sólida para nuestro proyecto. Aunque consideramos alternativas como AnthropicsAI, decidimos tirar por OpenAI ya que no vimos mejoras que justificasen el cambio.
        """
    )
    st.subheader("RAGs y Embeddings")
    st.write(
        """
        Buscando optimizar nuestro Modelo de Lenguaje de Gran Escala (LLM), inicialmente implementamos una solución basada en RAG (Retrieval-Augmented Generation) on-premise, con el modelo intfloat/e5-base-v2. A pesar de que los resultados iniciales fueron prometedores, la precisión en la conversión pregunta-embeddings por parte del RAG resultó insuficiente. Esto nos llevó a adoptar Fusion-RAG, una variante avanzada que integra otro LLM especializado para mejorar la generación de respuestas contextualmente relevantes y precisas, logrando así un rendimiento significativamente superior.

        Nos inspiramos en el trabajo de investigación arXiv:2402.03367, donde se explora las implicaciones y beneficios de esta tecnología en el campo de AI & LLM.
        """
    )
    st.subheader("Vector Databse")
    st.write(
        """
        Para enriquecer la capacidad de respuesta de LexAnalytica, hemos incorporado un Vector Store con una colección de legislación del BOE, junto con una variedad de documentos como resúmenes y exámenes corregidos. Por conveniencia, hemos optado por la infraestructura de Pinecone, donde alojamos nuestros embeddings, facilitando así un acceso rápido y seguro a la información.
        """
    )

show_creator_acknowledgement()
