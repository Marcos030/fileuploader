# AI_GENERATED_CODE_START
# [AI Generated] Data: 19/03/2024
# Descrição: Criação do guia de deploy para Streamlit Cloud
# Gerado por: Cursor AI
# Versão: Streamlit Cloud
# AI_GENERATED_CODE_END

# 🚀 Guia de Deploy no Streamlit Cloud

Este guia irá ajudá-lo a fazer o deploy da aplicação Q&A com IA no Streamlit Cloud.

## 📋 Pré-requisitos

1. **Conta no GitHub**
   - Crie uma conta em [GitHub](https://github.com) se ainda não tiver

2. **Conta no Streamlit Cloud**
   - Acesse [Streamlit Cloud](https://streamlit.io/cloud)
   - Faça login com sua conta GitHub

3. **API Key do OpenAI**
   - Obtenha sua chave em [OpenAI Platform](https://platform.openai.com/api-keys)

## 🔄 Passo a Passo

### 1. Preparar o Repositório

1. **Fork do repositório**
   - Clique em "Fork" no canto superior direito
   - Isso criará uma cópia em sua conta GitHub

2. **Verificar arquivos**
   - Confirme que os seguintes arquivos estão presentes:
     - `streamlit_app.py` (arquivo principal)
     - `requirements.txt` (dependências Python)
     - `packages.txt` (dependências do sistema)
     - `.streamlit/config.toml` (configuração do Streamlit)

### 2. Configurar no Streamlit Cloud

1. **Acessar Streamlit Cloud**
   - Vá para [share.streamlit.io](https://share.streamlit.io)
   - Faça login com sua conta GitHub

2. **Criar novo app**
   - Clique em "New app"
   - Selecione seu repositório forkado
   - Configure:
     - **Repository**: Seu repositório forkado
     - **Branch**: main (ou master)
     - **Main file path**: `streamlit_app.py`

3. **Configurar Secrets**
   - Clique em "Advanced settings"
   - Vá para a aba "Secrets"
   - Adicione sua API Key:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```

4. **Deploy**
   - Clique em "Deploy!"
   - Aguarde o processo de build (pode levar alguns minutos)

### 3. Verificar o Deploy

1. **Testar a aplicação**
   - Acesse a URL fornecida pelo Streamlit Cloud
   - Teste o upload de um arquivo
   - Faça uma pergunta para verificar se está funcionando

2. **Verificar logs**
   - Se houver problemas, verifique os logs em "Settings" > "Logs"

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

No Streamlit Cloud, você pode configurar variáveis adicionais:

```toml
OPENAI_API_KEY = "sk-..."
OPENAI_ORG_ID = "org-..."  # Opcional
OPENAI_BASE_URL = "https://api.openai.com/v1"  # Opcional
```

### Configurações de Performance

O arquivo `.streamlit/config.toml` já está otimizado para produção:

- `maxUploadSize = 200` (limite de 200MB)
- `headless = true` (modo headless para servidor)
- `enableCORS = false` (desabilita CORS para melhor performance)

## 🐛 Solução de Problemas

### Erro de Build

1. **Verificar dependências**
   - Confirme que `requirements.txt` está correto
   - Verifique se `packages.txt` está presente

2. **Verificar sintaxe**
   - Teste localmente: `streamlit run streamlit_app.py`
   - Corrija erros de sintaxe antes do deploy

### Erro de API Key

1. **Verificar Secrets**
   - Confirme que a API Key está correta
   - Verifique se tem créditos na conta OpenAI

2. **Formato correto**
   - A API Key deve começar com `sk-`
   - Não deve ter espaços extras

### Erro de Memória

1. **Reduzir tamanho de arquivos**
   - Use arquivos menores para teste
   - Reduza o tamanho dos chunks

2. **Otimizar configurações**
   - Ajuste `maxUploadSize` no config.toml
   - Reduza `max_tokens` na aplicação

## 📊 Monitoramento

### Logs do Streamlit Cloud

- Acesse "Settings" > "Logs" para ver logs em tempo real
- Útil para debug de problemas

### Métricas de Uso

- Monitore o uso da API OpenAI
- Verifique o consumo de recursos

## 🔒 Segurança

### Proteção de Dados

- API Keys são armazenadas de forma segura
- Arquivos são processados temporariamente
- Nenhum dado é armazenado permanentemente

### Boas Práticas

- Nunca commite API Keys no código
- Use sempre o sistema de Secrets do Streamlit Cloud
- Monitore o uso da API regularmente

## 🔄 Atualizações

### Atualizar o App

1. **Fazer mudanças no código**
2. **Commit e push para GitHub**
3. **Streamlit Cloud fará deploy automático**

### Atualizar Secrets

1. Vá em "Settings" > "Secrets"
2. Edite as variáveis necessárias
3. Salve as alterações

## 📞 Suporte

- **Streamlit Cloud**: [Documentação oficial](https://docs.streamlit.io/streamlit-community-cloud)
- **GitHub Issues**: Use a aba Issues do repositório
- **Stack Overflow**: Tag `streamlit`

---

**🎉 Parabéns! Sua aplicação está no ar!** 