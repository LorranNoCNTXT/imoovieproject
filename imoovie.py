import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3


def inicializar_banco():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            nick TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()


def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nick=? AND senha=?', (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()
    if resultado:
        mostrar_categoria()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")


def mensagem_clicavel(event):
    mostrar_cadastro()


def mostrar_login():
    limpar_tela()
    frame_login = tk.Frame(root, bg='black')
    frame_login.pack(expand=True, fill='both')

    adicionar_logo(frame_login)

    frame_conteudo = tk.Frame(frame_login, bg='black')
    frame_conteudo.pack(expand=True)

    label_usuario = tk.Label(frame_conteudo, text="Usuário:", fg='#483D8B', bg='black', font=20)
    label_usuario.pack(pady=6)

    global entry_usuario
    entry_usuario = tk.Entry(frame_conteudo)
    entry_usuario.pack(pady=6)

    label_senha = tk.Label(frame_conteudo, text="Senha:", fg='#483D8B', bg='black', font=20)
    label_senha.pack(pady=6)

    global entry_senha
    entry_senha = tk.Entry(frame_conteudo, show="*")
    entry_senha.pack(pady=6)

    botao_login = tk.Button(frame_conteudo, text="Login", command=verificar_login, bg='#483D8B', fg='white')
    botao_login.pack(pady=40)

    frase_clicavel = tk.Label(frame_conteudo, text="Novo no Imoovie? Faça seu cadastro agora mesmo!", fg='white',
                              bg='black', font=20)
    frase_clicavel.pack(pady=20)
    frase_clicavel.bind("<Button-1>", mensagem_clicavel)
    frase_clicavel.bind("<Enter>", lambda e: frase_clicavel.config(cursor="hand2"))
    frase_clicavel.bind("<Leave>", lambda e: frase_clicavel.config(cursor=""))


def mostrar_cadastro():
    limpar_tela()
    frame_cadastro = tk.Frame(root, bg='black')
    frame_cadastro.pack(expand=True, fill='both')

    adicionar_logo(frame_cadastro)

    frame_conteudo = tk.Frame(frame_cadastro, bg='black')
    frame_conteudo.pack(expand=True)

    tk.Label(frame_conteudo, text="Nome:", fg='#483D8B', bg='black').pack(pady=5)
    entry_nome = tk.Entry(frame_conteudo)
    entry_nome.pack(pady=5)

    tk.Label(frame_conteudo, text="Sobrenome:", fg='#483D8B', bg='black').pack(pady=5)
    entry_sobrenome = tk.Entry(frame_conteudo)
    entry_sobrenome.pack(pady=5)

    tk.Label(frame_conteudo, text="Nick:", fg='#483D8B', bg='black').pack(pady=5)
    entry_nick = tk.Entry(frame_conteudo)
    entry_nick.pack(pady=5)

    tk.Label(frame_conteudo, text="Senha:", fg='#483D8B', bg='black').pack(pady=5)
    entry_senha = tk.Entry(frame_conteudo, show="*")
    entry_senha.pack(pady=5)

    tk.Label(frame_conteudo, text="Telefone:", fg='#483D8B', bg='black').pack(pady=5)
    entry_telefone = tk.Entry(frame_conteudo)
    entry_telefone.pack(pady=5)

    tk.Label(frame_conteudo, text="Email:", fg='#483D8B', bg='black').pack(pady=5)
    entry_email = tk.Entry(frame_conteudo)
    entry_email.pack(pady=5)

    botao_registrar = tk.Button(frame_conteudo, text="Registrar", command=lambda: cadastrar(
        entry_nome.get(), entry_sobrenome.get(), entry_nick.get(),
        entry_senha.get(), entry_telefone.get(), entry_email.get()))
    botao_registrar.pack(pady=20)

    adicionar_botao_voltar(frame_cadastro, lambda: mostrar_login())


def cadastrar(nome, sobrenome, nick, senha, telefone, email):
    if not all([nome, sobrenome, nick, senha, telefone, email]):
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return
    try:
        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, sobrenome, nick, senha, telefone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, sobrenome, nick, senha, telefone, email))
        conexao.commit()
        messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Nick ou email já cadastrados.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        conexao.close()


def mostrar_categoria():
    limpar_tela()
    frame_categoria = tk.Frame(root, bg='black')
    frame_categoria.pack(expand=True, fill='both')

    adicionar_logo(frame_categoria)

    categoria_label = tk.Label(frame_categoria, text="Escolha uma categoria", fg='#483D8B', bg='black',
                               font=("Helvetica", 18))
    categoria_label.pack(pady=10)

    categorias = ["Filmes", "Séries", "Jogos", "Animes"]
    for categoria in categorias:
        categoria_botao = tk.Button(frame_categoria, text=categoria, bg='white', fg='black', width=15)
        categoria_botao.pack(pady=5)
        if categoria == "Filmes":
            categoria_botao.config(command=mostrar_filmes)
        if categoria == "Séries":
            categoria_botao.config(command=mostrar_series)
        if categoria == "Jogos":
            categoria_botao.config(command=mostrar_jogos)
        if categoria == "Animes":
            categoria_botao.config(command=mostrar_animes)

    adicionar_botao_voltar(frame_categoria, lambda: mostrar_login())


def mostrar_jogos():
    limpar_tela()
    frame_jogos = tk.Frame(root, bg='black')
    frame_jogos.pack(expand=True, fill='both')
    adicionar_logo(frame_jogos)
    adicionar_botao_voltar(frame_jogos, lambda: mostrar_categoria())


def mostrar_animes():
    limpar_tela()
    frame_animes = tk.Frame(root, bg='black')
    frame_animes.pack(expand=True, fill='both')
    adicionar_logo(frame_animes)
    adicionar_botao_voltar(frame_animes, lambda: mostrar_categoria())


def mostrar_series():
    limpar_tela()
    frame_series = tk.Frame(root, bg='black')
    frame_series.pack(expand=True, fill='both')
    adicionar_logo(frame_series)

    serie_label = tk.Label(frame_series, text="Escolha de serie", fg='#483D8B', bg='black', font=("Helvetica", 18))
    serie_label.pack(pady=10)

    serie = ["Stranger", "Fimose"]
    for serie in serie:
        serie_botao = tk.Button(frame_series, text=serie, bg='white', fg='black', width=30)
        serie_botao.pack(pady=5)
        if serie == "Stranger":
            serie_botao.config(command=mostrar_stranger)
        if serie == "Fimose":
            serie_botao.config(command=mostrar_fimose)

    adicionar_botao_voltar(frame_series, lambda: mostrar_categoria())


def mostrar_filmes():
    limpar_tela()
    frame_filmes = tk.Frame(root, bg='black')
    frame_filmes.pack(expand=True, fill='both')

    adicionar_logo(frame_filmes)

    filme_label = tk.Label(frame_filmes, text="Escolha de filme", fg='#483D8B', bg='black', font=("Helvetica", 18))
    filme_label.pack(pady=10)

    filmes = ["Deadpool", "Tropa De Elite"]
    for filme in filmes:
        filme_botao = tk.Button(frame_filmes, text=filme, bg='white', fg='black', width=30)
        filme_botao.pack(pady=5)
        if filme == "Deadpool":
            filme_botao.config(command=mostrar_deadpool)
        if filme == "Tropa De Elite":
            filme_botao.config(command=mostrar_tropadeelite)

    adicionar_botao_voltar(frame_filmes, lambda: mostrar_categoria())


def mostrar_deadpool():
    limpar_tela()
    frame_deadpool = tk.Frame(root, bg='black')
    frame_deadpool.pack(expand=True, fill='both')
    adicionar_logo(frame_deadpool)
    adicionar_botao_voltar(frame_deadpool, lambda: mostrar_filmes())


def mostrar_tropadeelite():
    limpar_tela()
    frame_tropadeelite = tk.Frame(root, bg='black')
    frame_tropadeelite.pack(expand=True, fill='both')
    adicionar_logo(frame_tropadeelite)
    adicionar_botao_voltar(frame_tropadeelite, lambda: mostrar_filmes())


def mostrar_stranger():
    limpar_tela()
    frame_stranger = tk.Frame(root, bg='black')
    frame_stranger.pack(expand=True, fill='both')
    adicionar_logo(frame_stranger)
    adicionar_botao_voltar(frame_stranger, lambda: mostrar_series())


def mostrar_fimose():
    limpar_tela()
    frame_fimose = tk.Frame(root, bg='black')
    frame_fimose.pack(expand=True, fill='both')
    adicionar_logo(frame_fimose)
    adicionar_botao_voltar(frame_fimose, lambda: mostrar_series())


def adicionar_logo(frame):
    logo_imagem = Image.open("logo.png")
    logo_imagem = logo_imagem.resize((150, 150), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_imagem)
    label_logo = tk.Label(frame, image=logo_photo, bg='black')
    label_logo.image = logo_photo
    label_logo.pack(pady=20)


def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()


def adicionar_botao_voltar(frame, comando):
    botao_voltar = tk.Button(frame, text="Voltar", command=comando, bg='#483D8B', fg='white')
    botao_voltar.pack(pady=20)


root = tk.Tk()
root.title("Imoovie")
root.geometry("800x600")
inicializar_banco()
mostrar_login()
root.mainloop()
