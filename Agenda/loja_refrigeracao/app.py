import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime

# Configurações do banco de dados
conn = psycopg2.connect(
    dbname="loja_refrigeracao",
    user="postgres",  
    password="deivis",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Função para mostrar agendamentos
def mostrar_agendamentos():
    for i in tree.get_children():
        tree.delete(i)
    
    cursor.execute("SELECT nome, data_cadastro, endereco, problema, hora, valor, forma_pagamento FROM visitas")
    registros = cursor.fetchall()
    
    for registro in registros:
        data_cadastro = registro[1].strftime("%d/%m/%Y")  # Formatar a data
        hora = registro[4].strftime("%H:%M") if registro[4] else ""  # Formatar a hora se existir
        problema = registro[3] if registro[3] else ""  # Substituir None por string vazia
        valor = registro[5] if registro[5] else ""  # Valor pode ser vazio
        forma_pagamento = registro[6] if registro[6] else ""  # Forma de pagamento pode ser vazia
        tree.insert("", tk.END, values=(registro[0], data_cadastro, registro[2], problema, hora, valor, forma_pagamento))

# Função para cadastrar agendamentos
def cadastrar_agendamento():
    nome = nome_entry.get()
    data = data_entry.get()
    endereco = endereco_entry.get()
    problema = problema_entry.get() or ""  # Se não preencher, será uma string vazia
    hora = hora_entry.get() or None  # Se não preencher, será None
    valor = valor_entry.get() or None  # Se não preencher, será None
    forma_pagamento = forma_pagamento_var.get() or ""  # Se não preencher, será uma string vazia

    if not nome or not data or not endereco:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
        return

    try:
        data_cadastro = datetime.strptime(data, "%d/%m/%Y").date()  # Converte a string de data
        if hora:  # Se hora estiver preenchida, converte para TIME
            hora = datetime.strptime(hora, "%H:%M").time()
        
        cursor.execute("INSERT INTO visitas (nome, data_cadastro, endereco, problema, hora, valor, forma_pagamento) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (nome, data_cadastro, endereco, problema, hora, valor, forma_pagamento))
        conn.commit()
        mostrar_agendamentos()
        clear_entries()
        messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar agendamento: {e}")

# Função para excluir um agendamento
def excluir_agendamento():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um agendamento para excluir.")
        return

    agendamento_id = tree.item(selected_item)['values'][0]  # Pega o nome do agendamento
    cursor.execute("DELETE FROM visitas WHERE nome = %s", (agendamento_id,))
    conn.commit()
    mostrar_agendamentos()
    messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso!")

# Função para alterar um agendamento
def alterar_agendamento():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um agendamento para alterar.")
        return

    # Obtém os valores atuais
    nome = tree.item(selected_item)['values'][0]
    data = tree.item(selected_item)['values'][1]
    endereco = tree.item(selected_item)['values'][2]
    problema = tree.item(selected_item)['values'][3]
    hora = tree.item(selected_item)['values'][4]
    valor = tree.item(selected_item)['values'][5]
    forma_pagamento = tree.item(selected_item)['values'][6]

    # Preenche os campos com os valores existentes
    nome_entry.delete(0, tk.END)
    nome_entry.insert(0, nome)
    data_entry.delete(0, tk.END)
    data_entry.insert(0, datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y"))
    endereco_entry.delete(0, tk.END)
    endereco_entry.insert(0, endereco)
    problema_entry.delete(0, tk.END)
    problema_entry.insert(0, problema)
    hora_entry.delete(0, tk.END)
    if hora:
        hora_entry.insert(0, datetime.strptime(hora, "%H:%M").strftime("%H:%M"))
    valor_entry.delete(0, tk.END)
    valor_entry.insert(0, valor)
    forma_pagamento_var.set(forma_pagamento)

    # Alterar os dados após edição
    def salvar_alteracao():
        nome_novo = nome_entry.get()
        data_nova = data_entry.get()
        endereco_novo = endereco_entry.get()
        problema_novo = problema_entry.get() or ""  # Se não preencher, será uma string vazia
        hora_nova = hora_entry.get() or None  # Se não preencher, será None
        valor_novo = valor_entry.get() or None  # Se não preencher, será None
        forma_pagamento_nova = forma_pagamento_var.get() or ""  # Se não preencher, será uma string vazia

        if not nome_novo or not data_nova or not endereco_novo:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            data_nova_cadastro = datetime.strptime(data_nova, "%d/%m/%Y").date()  # Converte a string de data
            if hora_nova:  # Se hora estiver preenchida, converte para TIME
                hora_nova = datetime.strptime(hora_nova, "%H:%M").time()

            cursor.execute("UPDATE visitas SET nome = %s, data_cadastro = %s, endereco = %s, problema = %s, hora = %s, valor = %s, forma_pagamento = %s WHERE nome = %s",
                           (nome_novo, data_nova_cadastro, endereco_novo, problema_novo, hora_nova, valor_novo, forma_pagamento_nova, nome))
            conn.commit()
            mostrar_agendamentos()
            clear_entries()
            messagebox.showinfo("Sucesso", "Agendamento alterado com sucesso!")
            alterar_window.destroy()  # Fecha a janela de alteração
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar agendamento: {e}")

    # Cria uma nova janela para editar os dados
    alterar_window = tk.Toplevel(root)
    alterar_window.title("Alterar Agendamento")
    tk.Button(alterar_window, text="Salvar Alteração", command=salvar_alteracao).pack(pady=10)

# Função para limpar os campos de entrada
def clear_entries():
    nome_entry.delete(0, tk.END)
    data_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    problema_entry.delete(0, tk.END)
    hora_entry.delete(0, tk.END)
    valor_entry.delete(0, tk.END)
    forma_pagamento_var.set("")

# Função para formatar a entrada da data
def formatar_data(event):
    data = data_entry.get()
    if len(data) == 2 or len(data) == 5:
        data_entry.insert(len(data), '/')
    elif len(data) > 10:
        data_entry.delete(10, tk.END)

# Função para formatar a entrada da hora
def formatar_hora(event):
    hora = hora_entry.get()
    if len(hora) == 2:
        hora_entry.insert(len(hora), ':')
    elif len(hora) > 5:
        hora_entry.delete(5, tk.END)

# Criar interface gráfica
root = tk.Tk()
root.title("Agendamentos Loja de Refrigeração")

# Layout
frame = tk.Frame(root)
frame.pack(pady=10)

# Labels e Entradas
tk.Label(frame, text="Nome:").grid(row=0, column=0)
nome_entry = tk.Entry(frame)
nome_entry.grid(row=0, column=1)

tk.Label(frame, text="Data:").grid(row=1, column=0)
data_entry = tk.Entry(frame)
data_entry.grid(row=1, column=1)
data_entry.bind("<KeyRelease>", formatar_data)  # Formata data ao digitar

tk.Label(frame, text="Endereço:").grid(row=2, column=0)
endereco_entry = tk.Entry(frame)
endereco_entry.grid(row=2, column=1)

tk.Label(frame, text="Problema:").grid(row=3, column=0)
problema_entry = tk.Entry(frame)
problema_entry.grid(row=3, column=1)

tk.Label(frame, text="Hora:").grid(row=4, column=0)
hora_entry = tk.Entry(frame)
hora_entry.grid(row=4, column=1)
hora_entry.bind("<KeyRelease>", formatar_hora)  # Formata hora ao digitar

tk.Label(frame, text="Valor:").grid(row=5, column=0)
valor_entry = tk.Entry(frame)
valor_entry.grid(row=5, column=1)

tk.Label(frame, text="Forma de Pagamento:").grid(row=6, column=0)
forma_pagamento_var = tk.StringVar()
forma_pagamento_combobox = ttk.Combobox(frame, textvariable=forma_pagamento_var)
forma_pagamento_combobox['values'] = ('', 'Cartão', 'Dinheiro', 'Pix')
forma_pagamento_combobox.grid(row=6, column=1)

# Botões
tk.Button(frame, text="Cadastrar", command=cadastrar_agendamento).grid(row=7, column=0, pady=10)
tk.Button(frame, text="Alterar", command=alterar_agendamento).grid(row=7, column=1, pady=10)
tk.Button(frame, text="Excluir", command=excluir_agendamento).grid(row=7, column=2, pady=10)

# Tabela para exibir agendamentos
tree = ttk.Treeview(root, columns=("Nome", "Data", "Endereço", "Problema", "Hora", "Valor", "Forma de Pagamento"), show='headings')
tree.heading("Nome", text="Nome")
tree.heading("Data", text="Data")
tree.heading("Endereço", text="Endereço")
tree.heading("Problema", text="Problema")
tree.heading("Hora", text="Hora")
tree.heading("Valor", text="Valor")
tree.heading("Forma de Pagamento", text="Forma de Pagamento")
tree.pack(pady=20)

# Mostrar agendamentos ao iniciar
mostrar_agendamentos()

# Manter o terminal aberto
input("Pressione Enter para continuar...")

root.mainloop()

# Fechar conexão ao final
cursor.close()
conn.close()
