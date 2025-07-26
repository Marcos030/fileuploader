# AI_GENERATED_CODE_START
# [AI Generated] Data: 19/03/2024
# Descrição: Atualização do streamlit_app.py para resolver problema de compatibilidade do SQLite3
# Gerado por: Cursor AI
# Versão: Streamlit 1.28.0+, LangChain 0.1.0+
# AI_GENERATED_CODE_END

import os
import tempfile
import pandas as pd
import pytesseract
from PIL import Image
import docx
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from pypdf.errors import PdfReadError
from openai import AuthenticationError, BadRequestError

# Configuração da página
st.set_page_config(
    page_title="Q&A com IA - PLN usando LangChain",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar variáveis de ambiente
load_dotenv()

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    .file-uploader {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da aplicação
st.markdown('<h1 class="main-header">🤖 Q&A com IA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Processamento de Linguagem Natural usando LangChain</p>', unsafe_allow_html=True)

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Configuração da API Key
    api_key_method = st.radio(
        "Método de configuração da API Key:",
        ["Arquivo .env", "Input manual"]
    )
    
    if api_key_method == "Input manual":
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Insira sua chave da API OpenAI"
        )
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        # Verificar se a chave está no arquivo .env
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            st.success("✅ API Key encontrada no arquivo .env")
        else:
            st.error("❌ API Key não encontrada no arquivo .env")
            st.info("Crie um arquivo .env na raiz do projeto com: OPENAI_API_KEY=sua_chave_aqui")
    
    # Configurações do modelo
    st.subheader("🔧 Configurações do Modelo")
    model_name = st.selectbox(
        "Modelo OpenAI:",
        ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo-preview"],
        index=0
    )
    
    temperature = st.slider(
        "Temperatura (criatividade):",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controla a criatividade das respostas"
    )
    
    max_tokens = st.slider(
        "Máximo de tokens:",
        min_value=100,
        max_value=4000,
        value=2000,
        step=100
    )

# Área principal
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Upload de Arquivo")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Escolha um arquivo para análise:",
        type=['pdf', 'txt', 'csv', 'docx', 'jpeg', 'jpg', 'png'],
        help="Suporta PDF, TXT, CSV, DOCX e imagens (JPEG, PNG)"
    )
    
    if uploaded_file is not None:
        # Mostrar informações do arquivo
        file_details = {
            "Nome": uploaded_file.name,
            "Tipo": uploaded_file.type,
            "Tamanho": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.json(file_details)

with col2:
    st.header("❓ Sua Pergunta")
    
    # Área de texto para perguntas
    user_question = st.text_area(
        "Digite sua pergunta sobre o documento:",
        height=150,
        placeholder="Ex: Qual é o tema principal do documento?",
        help="Faça perguntas específicas sobre o conteúdo do documento"
    )
    
    # Configurações avançadas
    with st.expander("⚙️ Configurações Avançadas"):
        chunk_size = st.slider(
            "Tamanho dos chunks:",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100
        )
        
        chunk_overlap = st.slider(
            "Sobreposição dos chunks:",
            min_value=0,
            max_value=500,
            value=200,
            step=50
        )
        
        select_k = st.slider(
            "Número de chunks relevantes:",
            min_value=1,
            max_value=10,
            value=3
        )
        
        chain_type = st.selectbox(
            "Tipo de cadeia:",
            ['stuff', 'map_reduce', 'refine', 'map_rerank'],
            help="Método de processamento das perguntas"
        )

# Função para carregar documentos
def load_document(file_path, file_type):
    """Carrega documentos de diferentes tipos de arquivo"""
    try:
        if file_type == 'application/pdf':
            loader = PyPDFLoader(file_path)
            return loader.load()
        elif file_type == 'text/plain':
            loader = TextLoader(file_path, encoding='utf-8')
            return loader.load()
        elif file_type == 'text/csv':
            df = pd.read_csv(file_path)
            return [{"page_content": df.to_string(), "metadata": {"source": file_path}}]
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text)
            return [{"page_content": "\n".join(full_text), "metadata": {"source": file_path}}]
        elif file_type in ['image/jpeg', 'image/png', 'image/jpg']:
            text = pytesseract.image_to_string(Image.open(file_path), lang='por+eng')
            return [{"page_content": text, "metadata": {"source": file_path}}]
        else:
            st.error(f"Tipo de arquivo não suportado: {file_type}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {str(e)}")
        return None

# Função de perguntas e respostas
def process_question(file_path, file_type, query, chain_type, k, chunk_size, chunk_overlap):
    """Processa a pergunta usando LangChain"""
    try:
        # Carregar documento
        documents = load_document(file_path, file_type)
        if not documents:
            return None
        
        # Dividir documentos em chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator="\n"
        )
        texts = text_splitter.split_documents(documents)
        
        if not texts:
            st.error("Não foi possível extrair texto do documento")
            return None
        
        # Criar embeddings
        embeddings = OpenAIEmbeddings()
        
        # Criar vectorstore
        db = Chroma.from_documents(texts, embeddings)
        
        # Configurar retriever
        retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        
        # Configurar modelo
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Criar cadeia de perguntas e respostas
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=True
        )
        
        # Processar pergunta
        result = qa_chain({"query": query})
        return result
        
    except PdfReadError as e:
        st.error(f"Erro ao ler arquivo PDF: {e}")
        return None
    except AuthenticationError as e:
        st.error(f"Erro de autenticação: {e}")
        return None
    except BadRequestError as e:
        st.error(f"Erro na requisição: {e}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")
        return None

# Função para exibir resultados
def display_results(result):
    """Exibe os resultados de forma organizada"""
    if result:
        # Resposta principal
        st.success("✅ Resposta gerada com sucesso!")
        
        # Mostrar resposta
        st.subheader("🤖 Resposta:")
        st.markdown(result["result"])
        
        # Mostrar documentos fonte
        if result.get("source_documents"):
            st.subheader("📄 Documentos fonte:")
            for i, doc in enumerate(result["source_documents"], 1):
                with st.expander(f"Documento fonte {i}"):
                    st.markdown(doc.page_content)
                    if hasattr(doc, 'metadata') and doc.metadata:
                        st.caption(f"Fonte: {doc.metadata.get('source', 'N/A')}")

# Botão de execução
if st.button("🚀 Processar Pergunta", type="primary"):
    if not uploaded_file:
        st.error("❌ Por favor, faça upload de um arquivo")
    elif not user_question.strip():
        st.error("❌ Por favor, digite uma pergunta")
    else:
        # Verificar API Key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.error("❌ API Key do OpenAI não configurada")
        else:
            with st.spinner("🔄 Processando sua pergunta..."):
                # Salvar arquivo temporariamente
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    # Processar pergunta
                    result = process_question(
                        tmp_file_path,
                        uploaded_file.type,
                        user_question,
                        chain_type,
                        select_k,
                        chunk_size,
                        chunk_overlap
                    )
                    
                    # Exibir resultados
                    display_results(result)
                    
                finally:
                    # Limpar arquivo temporário
                    if os.path.exists(tmp_file_path):
                        os.unlink(tmp_file_path)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Desenvolvido com ❤️ usando Streamlit e LangChain</p>
        <p>Suporte: PDF, TXT, CSV, DOCX, JPEG, PNG</p>
    </div>
    """,
    unsafe_allow_html=True
) 
