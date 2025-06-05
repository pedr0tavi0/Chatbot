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
import time

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

# Análise de Sentimento
def analisar_sentimento(texto):
    resultado = sentiment_pipeline(texto)[0]
    label = resultado['label'].lower()
    
    if "1" in label or "2" in label:
        return "negativo"
    elif "4" in label or "5" in label:
        return "positivo"
    else:
        return "neutro"

# Tipo de pergunta
def analisar_pergunta(user_text):
    tokens = nlp(user_text.lower())
    if any(token.text in ["onde", "originado", "origem", "criado", "país"] for token in tokens):
        return "lugar"
    elif any(token.text in ["quem", "inventou", "criou", "desenvolveu"] for token in tokens):
        return "pessoa"
    elif any(token.text in ["ingredientes", "feito", "como", "preparado", "cozido"] for token in tokens):
        return "ingredientes"
    return "geral"

# Encontrar resposta
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

# Padronizar Mensagens
def exibir_mensagem(texto, autor="bot", sentimento="neutro"):
    chat_area.config(state='normal')

    cores = {
        "positivo": ("#d4edda", "#155724"),
        "negativo": ("#f8d7da", "#721c24"),
        "neutro": ("#cce5ff", "#004085"),
        "usuario": ("#e2e3e5", "#383d41")
    }

    bg_color, fg_color = cores.get(sentimento if autor == "bot" else "usuario", ("white", "black"))

    label = tk.Label(
        chat_area,
        text=texto,
        bg=bg_color,
        fg=fg_color,
        font=("Arial", 12),
        wraplength=400,
        justify="right" if autor == "usuario" else "left",
        padx=10,
        pady=5,
        anchor='e' if autor == "usuario" else 'w'
    )
    chat_area.window_create(tk.END, window=label)
    chat_area.insert(tk.END, "\n")  # Apenas 1 quebra de linha
    chat_area.config(state='disabled')
    chat_area.see(tk.END)

# Enviar pergunta
def send_message(text=None):
    user_text = text if text else user_input.get()
    if not user_text.strip():
        return

    exibir_mensagem(f"Você: {user_text}", autor="usuario")
    user_input.delete(0, tk.END)

    typing_label = tk.Label(
        chat_area,
        text="🤖 Bot está digitando...",
        bg="#fff3cd",
        fg="#856404",
        font=("Arial", 11, "italic"),
        wraplength=400,
        justify="left",
        padx=10,
        pady=5,
        anchor='w'
    )

    chat_area.config(state='normal')
    chat_area.window_create(tk.END, window=typing_label)
    chat_area.insert(tk.END, "\n")
    chat_area.config(state='disabled')
    chat_area.see(tk.END)

    def bot_response():
        time.sleep(1)
        resposta = encontrar_resposta(user_text)
        sentimento = analisar_sentimento(user_text)

        typing_label.destroy()
        exibir_mensagem(f"🤖 Bot ({sentimento}): {resposta}", autor="bot", sentimento=sentimento)

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

    if not texto.strip():
        return  # Evita enviar mensagem vazia
    send_message(texto)

def quit_app():
    if messagebox.askokcancel("Sair", "Tem certeza que deseja sair?"):
        window.destroy()

# Coleta do conteúdo
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
window.geometry("800x560")
window.config(bg="#fefefe")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled', bg="white", fg="black", font=("Arial", 12))
chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

right_frame = tk.Frame(window, bg="#e6f2ff")
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=0)

suggestion_frame = tk.Frame(right_frame, bg="#e6f2ff")
suggestion_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(suggestion_frame, text="Sugestões de Perguntas:", bg="#e6f2ff", font=("Arial", 10, "bold")).pack(pady=5)

for pergunta in perguntas_sugeridas:
    btn = tk.Button(suggestion_frame, text=pergunta, width=40, wraplength=200, anchor="w",
                    justify="left", command=lambda p=pergunta: send_message(p))
    btn.pack(pady=2)

input_frame = tk.Frame(right_frame, bg="#fefefe")
input_frame.pack(fill=tk.X, pady=0)

user_input = tk.Entry(input_frame, font=("Arial", 12))
user_input.pack(fill=tk.X, padx=5, pady=5)

button_frame = tk.Frame(input_frame, bg="#fefefe")
button_frame.pack(pady=5)

send_button = tk.Button(button_frame, text="Enviar", command=send_message, bg="#4CAF50", fg="white", font=("Arial", 12), width=10)
send_button.grid(row=0, column=0, padx=5)

mic_button = tk.Button(button_frame, text="🎤 Falar", command=reconhecer_fala, bg="#2196F3", fg="white", font=("Arial", 12), width=10)
mic_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(button_frame, text="Sair", command=quit_app, bg="#f44336", fg="white", font=("Arial", 12), width=10)
exit_button.grid(row=0, column=2, padx=5)

chat_area.tag_config('user', foreground='black', justify='right')
chat_area.tag_config('bot_positivo_left', foreground='green', justify='left')
chat_area.tag_config('bot_neutro_left', foreground='blue', justify='left')
chat_area.tag_config('bot_negativo_left', foreground='red', justify='left')

window.mainloop()
