# AI_GENERATED_CODE_START
# [AI Generated] Data: 19/03/2024
# Descrição: Atualização completa do README.md com instruções detalhadas para deploy no Streamlit Cloud
# Gerado por: Cursor AI
# Versão: Streamlit 1.28.0+, LangChain 0.1.0+
# AI_GENERATED_CODE_END

# 🤖 Q&A com IA - PLN usando LangChain

Uma aplicação web interativa para fazer perguntas sobre documentos usando Processamento de Linguagem Natural (PLN) com LangChain e OpenAI.

## ✨ Funcionalidades

- **Upload de múltiplos formatos**: PDF, TXT, CSV, DOCX, JPEG, PNG
- **Processamento de imagens**: OCR automático para extrair texto de imagens
- **Interface intuitiva**: Interface web moderna e responsiva com Streamlit
- **Configurações flexíveis**: Ajuste de parâmetros do modelo e processamento
- **Respostas contextuais**: Respostas baseadas no conteúdo específico do documento
- **Documentos fonte**: Visualização dos trechos relevantes utilizados na resposta

## 🚀 Deploy no Streamlit Cloud

### Método 1: Deploy Automático (Recomendado)

1. **Fork do repositório**
   - Faça um fork deste repositório para sua conta GitHub

2. **Configurar variáveis de ambiente**
   - No Streamlit Cloud, vá em Settings > Secrets
   - Adicione sua chave da API OpenAI:
   ```toml
   OPENAI_API_KEY = "sua_chave_aqui"
   ```

3. **Deploy**
   - Conecte seu repositório ao Streamlit Cloud
   - O arquivo principal é `streamlit_app.py`
   - Deploy automático será realizado

### Método 2: Deploy Manual

1. **Clonar o repositório**
   ```bash
   git clone <url-do-seu-repositorio>
   cd fileUploader
   ```

2. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar API Key**
   - Crie um arquivo `.env` na raiz do projeto:
   ```
   OPENAI_API_KEY=sua_chave_aqui
   ```

4. **Executar localmente**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📋 Pré-requisitos

- **Python**: 3.8 ou superior
- **OpenAI API Key**: Chave válida da API OpenAI
- **Tesseract OCR**: Para processamento de imagens (instalado automaticamente no Streamlit Cloud)

## 🛠️ Instalação Local

### 1. Clonar o projeto
```bash
git clone <url-do-repositorio>
cd fileUploader
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sua_chave_aqui
```

### 5. Executar a aplicação
```bash
streamlit run streamlit_app.py
```

## 🔧 Configurações

### Parâmetros do Modelo
- **Modelo**: Escolha entre GPT-4, GPT-3.5-turbo ou GPT-4-turbo-preview
- **Temperatura**: Controla a criatividade das respostas (0.0 - 2.0)
- **Máximo de tokens**: Limite de tokens para a resposta

### Parâmetros de Processamento
- **Tamanho dos chunks**: Tamanho dos segmentos de texto (500-2000)
- **Sobreposição**: Sobreposição entre chunks para melhor contexto
- **Chunks relevantes**: Número de trechos considerados para a resposta
- **Tipo de cadeia**: Método de processamento (stuff, map_reduce, refine, map_rerank)

## 📁 Estrutura do Projeto

```
fileUploader/
├── streamlit_app.py      # Aplicação principal
├── requirements.txt      # Dependências Python
├── README.md            # Documentação
├── .env                 # Variáveis de ambiente (criar)
├── app.py              # Versão anterior
└── fileUploader.py     # Versão anterior
```

## 🔑 Configuração da API OpenAI

### Obter API Key
1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Faça login ou crie uma conta
3. Vá em "API Keys"
4. Crie uma nova chave de API

### Configurar no Streamlit Cloud
1. Acesse seu app no Streamlit Cloud
2. Vá em "Settings" > "Secrets"
3. Adicione:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```

### Configurar localmente
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sk-...
```

## 🎯 Como Usar

1. **Upload do documento**
   - Clique em "Browse files" e selecione seu documento
   - Formatos suportados: PDF, TXT, CSV, DOCX, JPEG, PNG

2. **Configurar parâmetros**
   - Ajuste as configurações na sidebar conforme necessário
   - Configure sua API Key se necessário

3. **Fazer pergunta**
   - Digite sua pergunta na área de texto
   - Seja específico para obter melhores respostas

4. **Processar**
   - Clique em "🚀 Processar Pergunta"
   - Aguarde o processamento

5. **Visualizar resultados**
   - A resposta será exibida na tela
   - Documentos fonte podem ser expandidos para verificação

## 🐛 Solução de Problemas

### Erro de API Key
- Verifique se a chave está correta
- Confirme se tem créditos disponíveis na conta OpenAI

### Erro de processamento de PDF
- Verifique se o PDF não está protegido por senha
- Confirme se o PDF contém texto (não apenas imagens)

### Erro de OCR
- Para imagens, certifique-se de que têm boa qualidade
- Texto deve estar legível e bem contrastado

### Erro de memória
- Reduza o tamanho dos chunks
- Use documentos menores
- Ajuste o número de chunks relevantes

## 📊 Formatos Suportados

| Formato | Extensão | Descrição |
|---------|----------|-----------|
| PDF | .pdf | Documentos PDF com texto |
| Texto | .txt | Arquivos de texto simples |
| CSV | .csv | Dados tabulares |
| Word | .docx | Documentos do Microsoft Word |
| Imagem | .jpg, .jpeg, .png | Imagens com texto (OCR) |

## 🔒 Segurança

- API Keys são armazenadas de forma segura
- Arquivos são processados temporariamente
- Nenhum dado é armazenado permanentemente
- Conexões são feitas via HTTPS

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- **Issues**: Use a aba Issues do GitHub
- **Documentação**: Consulte este README
- **Streamlit**: [Documentação oficial](https://docs.streamlit.io/)
- **LangChain**: [Documentação oficial](https://python.langchain.com/)

## 🔄 Atualizações

- **v2.0**: Interface redesenhada, melhor tratamento de erros
- **v1.0**: Versão inicial com funcionalidades básicas

---

**Desenvolvido com ❤️ usando Streamlit e LangChain**
