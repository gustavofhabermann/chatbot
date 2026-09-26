import random
import tkinter as tk
from tkinter import ttk, scrolledtext

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Carrega o modelo de português do spaCy
nlp = spacy.load("pt_core_news_sm")


# ---------------------------------------------------------------------------
# 1. Bot de boas-vindas
# ---------------------------------------------------------------------------

welcome_words_input = [
    "oi",
    "ola",
    "olá",
    "eae",
    "bom",
    "boa"
]

welcome_words_output = [
    "Olá!",
    "Oi, tudo bem?",
    "Olá, como posso ajudar?",
    "Oi! Vamos falar sobre Excel?"
]


def welcome_message(text):
    for word in text.split():
        if word.lower() in welcome_words_input:
            return random.choice(welcome_words_output)

    return None


# ---------------------------------------------------------------------------
# 2. Base de conhecimento - funções básicas do Excel
# ---------------------------------------------------------------------------

base_conhecimento = {

    "SOMA": [
        "A função SOMA adiciona todos os números presentes em um intervalo de células selecionado.",

        "Para usar a função SOMA basta digitar =SOMA(A1:A10) e o Excel retorna o total dos valores dessas células.",

        "A função SOMA é uma das funções mais básicas e utilizadas para totalizar colunas ou linhas de valores numéricos."
    ],

    "MÉDIA": [
        "A função MÉDIA calcula a média aritmética dos valores de um intervalo de células.",

        "Para calcular a média utiliza-se a fórmula =MÉDIA(A1:A10), que soma os valores e divide pela quantidade de células preenchidas.",

        "A função MÉDIA ignora células vazias no cálculo do resultado."
    ],

    "MÁXIMO": [
        "A função MÁXIMO retorna o maior valor numérico presente em um intervalo de células.",

        "A sintaxe da função é =MÁXIMO(A1:A10) e o resultado mostra o número mais alto do conjunto de dados."
    ],

    "MÍNIMO": [
        "A função MÍNIMO retorna o menor valor numérico presente em um intervalo de células.",

        "Utiliza-se a fórmula =MÍNIMO(A1:A10) para encontrar o menor número entre os valores selecionados."
    ],

    "CONT.SE": [
        "A função CONT.SE conta quantas células em um intervalo atendem a um determinado critério.",

        "A sintaxe é =CONT.SE(intervalo; critério), por exemplo contar valores maiores que cinco.",

        "A função CONT.SE é muito usada para contar ocorrências de um valor ou texto específico dentro de uma planilha."
    ],

    "SE": [
        "A função SE realiza um teste lógico e retorna um valor caso o resultado seja verdadeiro e outro valor caso seja falso.",

        "A sintaxe da função SE é =SE(teste_lógico; valor_se_verdadeiro; valor_se_falso).",

        "A função SE é utilizada para criar condições dentro de uma planilha, como aprovar ou reprovar um aluno de acordo com a nota."
    ],

    "PROCV": [
        "A função PROCV procura um valor na primeira coluna de uma tabela e retorna um valor correspondente de outra coluna.",

        "A sintaxe da função é =PROCV(valor_procurado; matriz_tabela; núm_coluna; procurar_intervalo).",

        "A função PROCV é muito utilizada para buscar informações relacionadas em grandes bases de dados, como preços de produtos em uma tabela."
    ],

    "CONCATENAR": [
        "A função CONCATENAR une o conteúdo de duas ou mais células em uma única célula de texto.",

        "A sintaxe da função é =CONCATENAR(A1;A2) e o resultado junta o texto das células indicadas.",

        "A função CONCATENAR pode ser substituída pelo operador & em versões mais recentes do Excel."
    ],

    "ARRED": [
        "A função ARRED arredonda um número para uma quantidade especificada de casas decimais.",

        "A sintaxe é =ARRED(número; num_dígitos), por exemplo =ARRED(3,456;2) retorna 3,46."
    ],

    "HOJE": [
        "A função HOJE retorna a data atual do sistema e é atualizada automaticamente sempre que a planilha é recalculada.",

        "A sintaxe da função é apenas =HOJE(), sem argumentos, pois ela usa a data do computador."
    ]
}


# ---------------------------------------------------------------------------
# 3. Transformando a base de conhecimento em uma lista de frases
# ---------------------------------------------------------------------------

original_sentences = []

for funcao, frases in base_conhecimento.items():

    for frase in frases:
        original_sentences.append(frase)


# ---------------------------------------------------------------------------
# 4. Pré-processamento
# ---------------------------------------------------------------------------

def preprocessing(sentence):

    sentence = sentence.lower()

    tokens = [
        token.text
        for token in nlp(sentence)
        if not (
            token.is_stop
            or token.like_num
            or token.is_punct
            or token.is_space
            or len(token) == 1
        )
    ]

    return " ".join(tokens)


# ---------------------------------------------------------------------------
# 5. TF-IDF + similaridade de cossenos
# ---------------------------------------------------------------------------

def answer(user_text, threshold=0.05):

    # Faz o pré-processamento das frases da base
    cleaned_sentences = [
        preprocessing(sentence)
        for sentence in original_sentences
    ]

    # Faz o pré-processamento da pergunta do usuário
    user_text_clean = preprocessing(user_text)

    # Adiciona a pergunta à lista
    cleaned_sentences.append(user_text_clean)

    # Cria o TF-IDF
    tfidf = TfidfVectorizer()

    # Transforma as frases em vetores
    x_sentences = tfidf.fit_transform(cleaned_sentences)

    # Calcula a similaridade entre a pergunta e todas as frases
    similarity = cosine_similarity(
        x_sentences[-1],
        x_sentences
    )

    # Pega o índice da frase mais semelhante
    sentence_index = similarity.argsort()[0][-2]

    # Pega o valor da similaridade
    similarity_value = similarity[0][sentence_index]

    # Verifica se a similaridade é suficiente
    if similarity_value < threshold:

        chatbot_answer = (
            "Desculpe, não encontrei uma resposta para essa função. "
            "Tente perguntar sobre SOMA, MÉDIA, MÁXIMO, MÍNIMO, CONT.SE, "
            "SE, PROCV, CONCATENAR, ARRED ou HOJE."
        )

    else:

        chatbot_answer = original_sentences[sentence_index]

    return chatbot_answer, similarity_value


# ---------------------------------------------------------------------------
# 6. Interface gráfica - Tkinter
# ---------------------------------------------------------------------------

class ChatbotExcelApp:

    def __init__(self, root):

        # Janela principal
        self.root = root

        self.root.title(
            "Chatbot — Funções Básicas do Excel"
        )

        self.root.geometry(
            "560x520"
        )

        self.root.resizable(
            False,
            False
        )


        # -------------------------------------------------------------------
        # Área de conversa
        # -------------------------------------------------------------------

        self.log = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state="disabled",
            font=("Segoe UI", 10)
        )

        self.log.pack(
            padx=10,
            pady=(10, 5),
            fill="both",
            expand=True
        )


        # Mensagem inicial do chatbot
        self._append_bot(
            "Olá! Sou um chatbot e posso explicar como funcionam "
            "as funções básicas do Excel.\n\n"
            "Escolha uma função na lista abaixo ou digite sua pergunta."
        )


        # -------------------------------------------------------------------
        # Linha com Combobox
        # -------------------------------------------------------------------

        frame_combo = ttk.Frame(root)

        frame_combo.pack(
            padx=10,
            pady=(0, 5),
            fill="x"
        )


        # Texto "Função:"
        ttk.Label(
            frame_combo,
            text="Função:"
        ).pack(
            side="left"
        )


        # Combobox com as funções
        self.combo = ttk.Combobox(
            frame_combo,
            values=list(base_conhecimento.keys()),
            state="readonly",
            width=15
        )

        self.combo.pack(
            side="left",
            padx=(5, 10)
        )


        # Botão explicar função
        ttk.Button(
            frame_combo,
            text="Explicar função",
            command=self.on_explain_click
        ).pack(
            side="left"
        )


        # -------------------------------------------------------------------
        # Campo para digitar perguntas
        # -------------------------------------------------------------------

        frame_entry = ttk.Frame(root)

        frame_entry.pack(
            padx=10,
            pady=(0, 10),
            fill="x"
        )


        # Campo de texto
        self.entry = ttk.Entry(
            frame_entry
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True
        )


        # Permite apertar ENTER para enviar
        self.entry.bind(
            "<Return>",
            lambda event: self.on_send_click()
        )


        # Botão enviar
        ttk.Button(
            frame_entry,
            text="Enviar",
            command=self.on_send_click
        ).pack(
            side="left",
            padx=(5, 0)
        )


    # -----------------------------------------------------------------------
    # Função para adicionar mensagem do usuário
    # -----------------------------------------------------------------------

    def _append_user(self, text):

        self.log.configure(
            state="normal"
        )

        self.log.insert(
            tk.END,
            f"Você: {text}\n\n"
        )

        self.log.configure(
            state="disabled"
        )

        self.log.see(
            tk.END
        )


    # -----------------------------------------------------------------------
    # Função para adicionar mensagem do chatbot
    # -----------------------------------------------------------------------

    def _append_bot(self, text):

        self.log.configure(
            state="normal"
        )

        self.log.insert(
            tk.END,
            f"Chatbot: {text}\n\n"
        )

        self.log.configure(
            state="disabled"
        )

        self.log.see(
            tk.END
        )


    # -----------------------------------------------------------------------
    # Ação do botão "Explicar função"
    # -----------------------------------------------------------------------

    def on_explain_click(self):

        # Pega a função selecionada
        funcao = self.combo.get()


        # Se nenhuma função foi selecionada
        if not funcao:
            return


        # Mostra a pergunta do usuário
        self._append_user(
            f"Explique a função {funcao}"
        )


        # Busca uma resposta usando TF-IDF
        resposta, similaridade = answer(
            f"o que é a função {funcao}"
        )


        # Mostra a resposta
        self._append_bot(
            resposta
        )


    # -----------------------------------------------------------------------
    # Ação do botão "Enviar"
    # -----------------------------------------------------------------------

    def on_send_click(self):

        # Pega o texto digitado
        texto = self.entry.get().strip()


        # Se estiver vazio, não faz nada
        if not texto:
            return


        # Limpa o campo de texto
        self.entry.delete(
            0,
            tk.END
        )


        # Mostra a mensagem do usuário
        self._append_user(
            texto
        )


        # Verifica se é uma saudação
        saudacao = welcome_message(
            texto
        )


        # Se for uma saudação
        if saudacao is not None:

            self._append_bot(
                saudacao
            )


        # Caso contrário, consulta a base de conhecimento
        else:

            resposta, similaridade = answer(
                texto
            )

            self._append_bot(
                resposta
            )


# ---------------------------------------------------------------------------
# 7. Inicialização do programa
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # Cria a janela
    root = tk.Tk()

    # Cria o aplicativo
    app = ChatbotExcelApp(
        root
    )

    # Mantém a janela aberta
    root.mainloop()