import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import font as tkfont
from io import BytesIO
import requests
import threading
import os


if os.path.exists("Poppins-Regular.ttf"):
    tkfont.Font(name="Poppins", file="Poppins-Regular.ttf", family="Poppins")

sns.set(style="whitegrid")

janela = tk.Tk()
janela.title("Análise de Cancelamento de Clientes")
janela.geometry("700x650")
janela.configure(bg='#f0f4f7')

def definir_icone_janela(janela, caminho_ico):
    try:
        janela.iconbitmap(caminho_ico)
    except Exception as e:
        print("Erro ao definir ícone da janela:", e)

definir_icone_janela(janela, "logo.ico")

def carregar_dados():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'gênero': np.random.choice(['Masculino', 'Feminino'], n),
        'idoso': np.random.choice([0, 1], n, p=[0.85, 0.15]),
        'tempo_de_contrato': np.random.randint(0, 72, n),
        'gastos_mensais': np.round(np.random.uniform(20, 120, n), 2),
        'tipo_de_contrato': np.random.choice(['Mensal', 'Anual', 'Semanal'], n, p=[0.6, 0.2, 0.2]),
        'forma_pagamento': np.random.choice([
            'Cartão de Crédito', 'Transferência Bancária',
            'Boleto Eletrônico', 'PIX'
        ], n),
    })
    df['gastos_totais'] = (df['tempo_de_contrato'] * df['gastos_mensais']) + np.random.normal(0, 100, n)
    
    df['cancelou'] = df['tipo_de_contrato'].apply(
        lambda x: np.random.choice(['Cancelado', 'Ativo'], p=[0.5, 0.5]) if x == 'Mensal'
        else np.random.choice(['Cancelado', 'Ativo'], p=[0.1, 0.9])
    )

    return df

def maximizar_janela_matplotlib():
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')
    except:
        try:
            mng.resize(*mng.window.maxsize())
        except:
            pass

def grafico_contrato():
    df = carregar_dados()
    df['cancelou'] = df['cancelou'].apply(lambda x: True if str(x).lower() in ['true', '1', 'sim', 'cancelado'] else False)

    df['cancelou_str'] = df['cancelou'].map({True: 'Cancelado', False: 'Ativo'})

    plt.figure()
    maximizar_janela_matplotlib()

    ax = sns.countplot(
        data=df,
        x='tipo_de_contrato',
        hue='cancelou_str',
        palette={
            'Ativo': '#228b22',        
            'Cancelado': '#a51c0b'     
        }
    )

    plt.title('Cancelamento por Tipo de Contratos')
    plt.xlabel('Tipo de Contratos')
    plt.ylabel('Número de Clientes')

    for container in ax.containers:
        ax.bar_label(container, fmt='%d', label_type='edge', padding=3)

    try:
        fig = plt.gcf()
        window = fig.canvas.manager.window
        window.title("Gráfico - Cancelamento de Clientes")
        window.iconbitmap("logo.ico")
    except Exception as e:
        print("Erro ao alterar ícone ou título da janela do gráfico:", e)

    plt.legend(title='Situação de Contratos')
    plt.tight_layout()
    plt.show()

def grafico_pagamento():
    df = carregar_dados()

    plt.figure()
    maximizar_janela_matplotlib()

    ax = sns.countplot(
        data=df,
        x='forma_pagamento',
        hue='cancelou',
        palette={
            'Ativo': '#228b22',
            'Cancelado': '#a51c0b'
        }
    )

    plt.title('Cancelamento por Forma de Pagamentos')
    plt.xticks(rotation=45)
    plt.xlabel('Formas de Pagamentos')
    plt.ylabel('Número de Clientes')

    for container in ax.containers:
        ax.bar_label(container, fmt='%d', label_type='edge', padding=3)

    try:
        fig = plt.gcf()
        window = fig.canvas.manager.window
        window.title("Gráfico - Cancelamento de Clientes")
        window.iconbitmap("logo.ico")
    except Exception as e:
        print("Erro ao alterar ícone ou título da janela do gráfico:", e)

    plt.legend(title='Situação de Pagamentos')
    plt.tight_layout()
    plt.show()

def grafico_gastos():
    df = carregar_dados()

    df['cancelou'] = df['cancelou'].apply(lambda x: True if str(x).lower() in ['true', '1', 'sim', 'cancelado'] else False)

    df['cancelou_str'] = df['cancelou'].map({True: 'Cancelado', False: 'Ativo'})

    plt.figure()
    maximizar_janela_matplotlib()

    ax = sns.boxplot(
        data=df,
        x='cancelou_str',
        y='gastos_mensais',
        palette={
            'Ativo': '#228b22',        
            'Cancelado': '#a51c0b'     
        }
    )

    medias = df.groupby('cancelou_str')['gastos_mensais'].mean()
    for i, (categoria, media) in enumerate(medias.items()):
        ax.text(i, media + 2, f'Média: R$ {media:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.title('Distribuição dos Gastos Mensais por Cancelamentos')
    plt.xlabel('Situação de Gastos Mensais')
    plt.ylabel('Gastos Mensais (R$)')

    try:
        fig = plt.gcf()
        window = fig.canvas.manager.window
        window.title("Gráfico - Cancelamento de Clientes")
        window.iconbitmap("logo.ico")
    except Exception as e:
        print("Erro ao alterar ícone ou título da janela do gráfico:", e)

    plt.tight_layout()
    plt.show()

def carregar_imagem_async(url, callback, tamanho=(24, 24)):
    def tarefa():
        try:
            response = requests.get(url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize(tamanho, Image.Resampling.LANCZOS)
            imagem = ImageTk.PhotoImage(img)
            janela.after(0, callback, imagem)
        except Exception as e:
            print(f"Erro ao carregar imagem de {url}:", e)
    threading.Thread(target=tarefa, daemon=True).start()

def carregar_logo():
    try:
        img = Image.open("logo.png")
        img = img.resize((180, 180), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(janela, image=logo, bg='#f0f4f7')
        logo_label.image = logo
        logo_label.pack(pady=10)
    except Exception as e:
        print("Erro ao carregar a logo local:", e)

carregar_logo()

titulo = tk.Label(
    janela,
    text="Visualização de Gráficos",
    font=('Poppins', 20, 'bold'),
    bg='#f0f4f7',
    fg='#333'
)
titulo.pack(pady=10)

style = ttk.Style()
style.configure('TButton', font=('Poppins', 11), padding=10)
style.map("TButton",
          background=[('active', '#d9e8f5')],
          foreground=[('pressed', 'black'), ('active', 'black')])

frame_botoes = tk.Frame(janela, bg='#f0f4f7')
frame_botoes.pack(pady=20)

btn1 = ttk.Button(frame_botoes, text="Tipos de Contratos", compound="left", command=grafico_contrato, width=30)
btn1.grid(row=0, column=0, pady=10)

btn2 = ttk.Button(frame_botoes, text="Formas de Pagamentos", compound="left", command=grafico_pagamento, width=30)
btn2.grid(row=1, column=0, pady=10)

btn3 = ttk.Button(frame_botoes, text="Gastos Mensais", compound="left", command=grafico_gastos, width=30)
btn3.grid(row=2, column=0, pady=10)

carregar_imagem_async(
    "https://cdn-icons-png.flaticon.com/512/5545/5545101.png",
    lambda img: btn1.configure(image=img) or setattr(btn1, 'image', img)
)

carregar_imagem_async(
    "https://static.vecteezy.com/system/resources/previews/013/484/039/original/secure-payment-3d-icon-png.png",
    lambda img: btn2.configure(image=img) or setattr(btn2, 'image', img)
)

carregar_imagem_async(
    "https://static.vecteezy.com/system/resources/previews/014/208/066/original/expense-ratio-3d-rendering-isometric-icon-png.png",
    lambda img: btn3.configure(image=img) or setattr(btn3, 'image', img)
)

footer = tk.Label(
    janela,
    text="Desenvolvido por Marco Medeiros | LinkedIn: linkedin.com/in/marco-medeirosdev",
    font=('Poppins', 10),
    bg='#f0f4f7',
    fg='gray'
)
footer.pack(side='bottom', pady=20)

janela.mainloop()