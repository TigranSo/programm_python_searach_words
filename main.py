import tkinter as tk
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import networkx as nx
import matplotlib.pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')

# Установка списка стоп-слов
stop_words = set(stopwords.words('russian'))


def create_keywords(text):
    words = word_tokenize(text.lower(), language='russian')
    words = [word for word in words if word.isalpha() and word not in stop_words]
    freq_dist = FreqDist(words)
    keywords = freq_dist.most_common(10)  # Выберем топ-10 ключевых слов
    return [word[0] for word in keywords]
# create_keywords принимает текст и возвращает список ключевых слов.
# Текст токенизируется, приводится к нижнему регистру, исключаются стоп-слова и неподходящие символы.
# Затем вычисляется частотное распределение слов и выбираются 10 наиболее часто встречающихся слов в виде ключевых.


def create_graph(keywords, text):
    G = nx.Graph()
    G.add_nodes_from(keywords)

    # Определение частоты слов в тексте
    freq_dist = FreqDist(word_tokenize(text.lower(), language='russian'))
    total_words = len(word_tokenize(text.lower(), language='russian'))

    # Рассчитываем вес ребра на основе частоты слов
    for i in range(len(keywords)):
        for j in range(i+1, len(keywords)):
            word1 = keywords[i]
            word2 = keywords[j]
            word1_freq = freq_dist[word1] / total_words
            word2_freq = freq_dist[word2] / total_words
            similarity = min(word1_freq, word2_freq)  
            G.add_edge(word1, word2, weight=similarity)

    return G
# create_graph принимает список ключевых слов и строит граф семантических связей между ними.
# Создается пустой граф G, в который добавляются узлы (ключевые слова).
# Затем для каждой пары слов добавляется ребро (сейчас устанавливается одинаковая связь между всеми парами).


def analyze():
    text = text_entry.get("1.0", tk.END)
    keywords = create_keywords(text)
    keyword_output.config(text=f"Ключевые слова: {', '.join(keywords)}")

    G = create_graph(keywords, text) 

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_weight='bold', font_size=10)
    plt.title("Граф семантических связей")
    plt.show()
# analyze извлекает текст из виджета text_entry.
# Создает список ключевых слов на основе текста и выводит их на виджет keyword_output.
# Создает граф семантических связей между ключевыми словами и отображает его с помощью библиотеки matplotlib.


root = tk.Tk()
root.title("Инструмент семантического анализа")
root.geometry('350x450+700+200')

text_label = tk.Label(root, text="Введите текст:")
text_label.pack()

text_entry = tk.Text(root, height=10, width=50)
text_entry.pack()

analyze_button = tk.Button(root, text="Анализировать текст", command=analyze)
analyze_button.pack()

keyword_output = tk.Label(root, text="Здесь будут отображаться ключевые слова")
keyword_output.pack()

root.mainloop()


