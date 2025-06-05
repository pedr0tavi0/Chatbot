import nltk
import spacy
import tkinter as tk
from tkinter import scrolledtext, messagebox
from goose3 import Goose
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
import threading
from transformers import pipeline
import speech_recognition as sr

# Análise de sentimento
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Baixar dados necessários
nltk.download('punkt')
nlp = spacy.load("pt_core_news_sm")

# Extrair texto da Wikipedia
def extrair_texto_wikipedia(url):
    g = Goose()
    artigo = g.extract(url)
    return sent_tokenize(artigo.cleaned_text)

# Pré-processamento de texto
def preprocessing(sentence):
    sentence = sentence.lower()
    tokens = [token.text for token in nlp(sentence) if not (token.is_stop or token.is_punct)]
    return " ".join(tokens)

# Analise de Sentimentos
def analisar_sentimento(texto):
    resultado = sentiment_pipeline(texto)[0]
    label = resultado['label']
    if "1" in label or "2" in label:
        return "negativo"
    elif "4" in label or "5" in label:
        return "positivo"
    else:
        return "neutro"

# Análise da pergunta
def analisar_pergunta(user_text):
    tokens = nlp(user_text.lower())
    if any(token.text in ["onde", "originado", "origem", "criado", "país"] for token in tokens):
        return "lugar"
    elif any(token.text in ["quem", "inventou", "criou", "desenvolveu"] for token in tokens):
        return "pessoa"
    elif any(token.text in ["ingredientes", "feito", "como", "preparado", "cozido"] for token in tokens):
        return "ingredientes"
    return "geral"

# Encontrar resposta com similaridade
def encontrar_resposta(user_text, threshold=0.1):
    tipo_pergunta = analisar_pergunta(user_text)
    frases_processadas = [preprocessing(frase) for frase in base_conhecimento]
    user_text = preprocessing(user_text)
    frases_processadas.append(user_text)
    tfidf = TfidfVectorizer()
    x_sentences = tfidf.fit_transform(frases_processadas)
    similarity = cosine_similarity(x_sentences[-1], x_sentences[:-1])
    max_index = similarity.argmax()
    max_value = similarity[0, max_index]
    if max_value < threshold:
        return "Não encontrei uma resposta precisa. Pode tentar reformular?"
    return base_conhecimento[max_index]

# Enviar pergunta
def send_message(text=None):
    user_text = text if text else user_input.get()
    if not user_text.strip():
        return
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"Você: {user_text}\n", 'user')
    chat_area.config(state='disabled')
    user_input.delete(0, tk.END)

    def bot_response():
        resposta = encontrar_resposta(user_text)
        sentimento = analisar_sentimento(user_text)

        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"🤖 Bot ({sentimento}): {resposta}\n", 'bot')
        chat_area.config(state='disabled')
        chat_area.see(tk.END)

    threading.Thread(target=bot_response).start()

def reconhecer_fala():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        chat_area.config(state='normal')
        chat_area.insert(tk.END, "🎤 Ouvindo...\n", 'bot')
        chat_area.config(state='disabled')
        chat_area.see(tk.END)
        try:
            audio = r.listen(source, timeout=5)
            texto = r.recognize_google(audio, language="pt-BR")
            send_message(texto)
        except sr.UnknownValueError:
            chat_area.config(state='normal')
            chat_area.insert(tk.END, "❌ Bot: Não entendi o que você disse.\n", 'bot')
            chat_area.config(state='disabled')
            chat_area.see(tk.END)
        except sr.WaitTimeoutError:
            chat_area.config(state='normal')
            chat_area.insert(tk.END, "⏱️ Bot: Tempo de escuta esgotado.\n", 'bot')
            chat_area.config(state='disabled')
            chat_area.see(tk.END)

def quit_app():
    if messagebox.askokcancel("Sair", "Tem certeza que deseja sair?"):
        window.destroy()

# Coleta de conteúdo da Wikipedia (culinária brasileira)
wiki_url = "https://pt.wikipedia.org/wiki/Culin%C3%A1ria_do_Brasil"
base_conhecimento = extrair_texto_wikipedia(wiki_url)

# Perguntas sugeridas
perguntas_sugeridas = [
"Como é feito o vatapá?", 
"Quais são os principais temperos usados na culinária baiana?",
"De onde é o cuscuz?", 
"Qual é a origem do tacacá?", 
"Quais pratos são típicos da culinária do Norte do Brasil?", 
"O que caracteriza a culinária brasileira?", 
"Quais são os doces típicos brasileiros?", 
"Quais influências a culinária de Mato Grosso tem?"
]

# Interface gráfica
window = tk.Tk()
window.title("Chatbot - Culinária Brasileira")
window.geometry("800x600")
window.config(bg="#fefefe")

# Área de chat
chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled', bg="white", fg="black", font=("Arial", 12))
chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

# Barra lateral com sugestões
suggestion_frame = tk.Frame(window, bg="#e6f2ff")
suggestion_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

tk.Label(suggestion_frame, text="Sugestões de Perguntas:", bg="#e6f2ff", font=("Arial", 10, "bold")).pack(pady=5)

for pergunta in perguntas_sugeridas:
    btn = tk.Button(suggestion_frame, text=pergunta, width=40, wraplength=200, anchor="w",
                    justify="left", command=lambda p=pergunta: send_message(p))
    btn.pack(pady=2)

# Campo de entrada do usuário
user_input = tk.Entry(window, font=("Arial", 14))
user_input.pack(fill=tk.X, padx=10, pady=(0, 10), side=tk.BOTTOM)

# Botões de envio, microfone e sair
button_frame = tk.Frame(window, bg="#fefefe")
button_frame.pack(pady=(0, 10), side=tk.BOTTOM)

send_button = tk.Button(button_frame, text="Enviar", command=send_message, bg="#4CAF50", fg="white", font=("Arial", 12), width=10)
send_button.grid(row=0, column=0, padx=5)

mic_button = tk.Button(button_frame, text="🎤 Falar", command=reconhecer_fala, bg="#2196F3", fg="white", font=("Arial", 12), width=10)
mic_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(button_frame, text="Sair", command=quit_app, bg="#f44336", fg="white", font=("Arial", 12), width=10)
exit_button.grid(row=0, column=2, padx=5)

# Estilo para textos
chat_area.tag_config('user', foreground='blue')
chat_area.tag_config('bot', foreground='green')

window.mainloop()