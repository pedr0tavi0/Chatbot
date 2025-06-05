# Chatbot Culinário Brasileiro 🇧🇷🤖

Este é um projeto de chatbot com interface gráfica em Tkinter, que responde a perguntas sobre **culinária brasileira**.  
Ele utiliza **Processamento de Linguagem Natural (NLP)** com **spaCy**, **análise de sentimentos** com modelos da **Hugging Face**, **reconhecimento de voz** e **similaridade semântica** para compreender e responder perguntas sobre pratos típicos, ingredientes, origens e muito mais.

---

## 🧠 Tecnologias utilizadas

- [Python 3.10+](https://www.python.org)
- [spaCy](https://spacy.io/) (`pt_core_news_sm`)
- [NLTK](https://www.nltk.org/)
- [Tkinter](https://wiki.python.org/moin/TkInter)
- [Goose3](https://github.com/goose3/goose3) (scraping e extração de texto da Wikipedia)
- [scikit-learn](https://scikit-learn.org/) (TF-IDF + Similaridade)
- [transformers](https://huggingface.co/transformers/) (Hugging Face – análise de sentimentos)
- [torch](https://pytorch.org/) (backend para os modelos da Hugging Face)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (reconhecimento de voz)
- [PyAudio](https://pypi.org/project/PyAudio/) (entrada de áudio)

---

## ⚙️ Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/chatbot-culinario.git
cd chatbot-culinario
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Se der erro com `pyaudio`, use:

```bash
pip install pipwin
pipwin install pyaudio
```

### 4. Baixe o modelo do spaCy

```bash
python -m spacy download pt_core_news_sm
```

### 5. Execute o chatbot

```bash
python chatbot_culinaria.py
```

---

## 🎙️ Recursos do Projeto 2

- ✅ Respostas com base em similaridade semântica (TF-IDF + cosine)
- ✅ Análise de sentimentos da pergunta com modelo Hugging Face (`nlptown/bert-base-multilingual-uncased-sentiment` ou equivalente)
- ✅ Reconhecimento de voz (opcional via microfone)
- ✅ Interface gráfica melhorada com sugestões de perguntas
- ✅ Extração automática de conhecimento direto da Wikipedia

---

## 💬 Exemplos de perguntas

- "Quem criou a feijoada?"
- "Onde foi originado o acarajé?"
- "Quais são os ingredientes da moqueca?"
- "Como é preparado o vatapá?"
- "O que é o baião de dois?"
- "Quais são os doces típicos brasileiros?"

---

## 🔍 Como funciona

1. **Extração de conhecimento**: o conteúdo da Wikipedia sobre Culinária do Brasil é coletado automaticamente com Goose3.
2. **Pré-processamento**: as frases são tokenizadas, normalizadas, e limpas com spaCy.
3. **Análise da pergunta**: o chatbot tenta entender o tipo de pergunta (origem, pessoa, ingredientes, etc.).
4. **Similaridade semântica**: a pergunta do usuário é comparada com frases do corpus usando TF-IDF e similaridade de cosseno.
5. **Análise de sentimento**: a pergunta também passa por um classificador de sentimento (neutro, positivo, negativo).
6. **Resposta**: a frase mais relevante é exibida, ou uma sugestão para reformular.

---

## 📌 Observações

- O chatbot responde melhor com perguntas relacionadas a pratos brasileiros.
- A qualidade das respostas depende do conteúdo extraído automaticamente da Wikipedia.
- Você pode expandir o conhecimento do bot trocando a URL ou combinando múltiplas fontes.

---

## 📁 Estrutura de Arquivos (sugerida)

```
chatbot-culinario/
├── chatbot_culinaria.py
├── requirements.txt
└── README.md
```

---

## 🤖 Futuras melhorias

- Geração de respostas com modelos de linguagem (ex: GPT-2 via Hugging Face)
- Suporte a mais temas culinários (ex: culinária internacional)
- Exportação do histórico de chat
- Versão web com Flask ou Streamlit
