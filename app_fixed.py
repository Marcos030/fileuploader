# AI_GENERATED_CODE_START
# [AI Generated] Data: 19/03/2024
# Descrição: Criação de versão corrigida do app.py com soluções para NumPy 2.0 e SQLite3
# Gerado por: Cursor AI
# Versão: Python 3.13+, NumPy 2.0+
# AI_GENERATED_CODE_END

# Solução para problemas de compatibilidade
import os
import sys

# Configurar variável de ambiente para usar DuckDB
os.environ['CHROMA_DB_IMPL'] = 'duckdb+parquet'

# Forçar versão compatível do NumPy
try:
    import numpy as np
    if not hasattr(np, 'float_'):
        # NumPy 2.0+ - adicionar compatibilidade
        np.float_ = np.float64
    if not hasattr(np, 'int_'):
        # NumPy 2.0+ - adicionar compatibilidade
        np.int_ = np.int64
    if not hasattr(np, 'uint'):
        # NumPy 2.0+ - adicionar compatibilidade
        np.uint = np.uint64
except ImportError:
    pass

import tempfile
import pandas as pd
import pytesseract
from PIL import Image
import docx
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from pypdf.errors import PdfReadError
from openai import AuthenticationError, BadRequestError

# Configuração da página
st.set_page_config(
    page_title="Q&A com IA - PLN usando LangChain",
    page_icon="🤖",
    layout="wide"
)

# Adicionar a imagem no cabeçalho
image_url = "https://cienciadosdados.com/images/CINCIA_DOS_DADOS_4.png"
st.image(image_url, use_column_width=True)

# Adicionar o nome do aplicativo
st.subheader("Q&A com IA - PLN usando LangChain")

# Componentes interativos
file_input = st.file_uploader("Upload a file", type=['pdf', 'txt', 'csv', 'docx', 'jpeg', 'png'])
openaikey = st.text_input("Enter your OpenAI API Key", type='password')
prompt = st.text_area("Enter your questions", height=160)
run_button = st.button("Run!")

select_k = st.slider("Number of relevant chunks", min_value=1, max_value=5, value=2)
select_chain_type = st.radio("Chain type", ['stuff', 'map_reduce', "refine", "map_rerank"])

# Função para carregar documentos
def load_document(file_path, file_type):
    if file_type == 'application/pdf':
        loader = PyPDFLoader(file_path)
        return loader.load()
    elif file_type == 'text/plain':
        loader = TextLoader(file_path)
        return loader.load()
    elif file_type == 'text/csv':
        df = pd.read_csv(file_path)
        return [{"page_content": df.to_string()}]
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return [{"page_content": "\n".join(full_text)}]
    elif file_type in ['image/jpeg', 'image/png']:
        text = pytesseract.image_to_string(Image.open(file_path))
        return [{"page_content": text}]
    else:
        st.error("Unsupported file type.")
        return None

# Função de perguntas e respostas
def qa(file_path, file_type, query, chain_type, k):
    try:
        documents = load_document(file_path, file_type)
        if not documents:
            return None
        
        # split the documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        
        # select which embeddings we want to use
        embeddings = OpenAIEmbeddings()
        
        # create the vectorestore to use as the index with DuckDB
        db = Chroma.from_documents(
            texts, 
            embeddings,
            persist_directory=None  # Não persistir para evitar problemas
        )
        
        # expose this index in a retriever interface
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
        
        # create a chain to answer questions 
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4"), 
            chain_type=chain_type, 
            retriever=retriever, 
            return_source_documents=True
        )
        result = qa({"query": query})
        return result
    except PdfReadError as e:
        st.error(f"Error reading PDF file: {e}")
        return None
    except AuthenticationError as e:
        st.error(f"Authentication error: {e}")
        return None
    except BadRequestError as e:
        st.error(f"Invalid request error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

# Função para exibir o resultado no Streamlit
def display_result(result):
    if result:
        st.markdown("### Result:")
        st.write(result["result"])
        st.markdown("### Relevant source text:")
        for doc in result["source_documents"]:
            st.markdown("---")
            st.markdown(doc.page_content)

# Execução do app
if run_button and file_input and openaikey and prompt:
    with st.spinner("Running QA..."):
        # Salvar o arquivo em um local temporário
        temp_file_path = os.path.join(tempfile.gettempdir(), file_input.name)
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_input.read())

        # Configurar a chave de API do OpenAI
        os.environ["OPENAI_API_KEY"] = openaikey

        # Verificar se a chave de API é válida
        try:
            # Testar a chave de API com uma chamada simples
            embeddings = OpenAIEmbeddings()
            embeddings.embed_documents(["test"])
        except AuthenticationError as e:
            st.error(f"Invalid OpenAI API Key: {e}")
        else:
            # Executar a função de perguntas e respostas
            result = qa(temp_file_path, file_input.type, prompt, select_chain_type, select_k)
            # Exibir o resultado
            display_result(result) 