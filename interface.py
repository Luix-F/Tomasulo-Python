import tkinter as tk
from tkinter import ttk
import tomasulo

t = tomasulo
toma = t.Tomasulo()
toma.simulador()

index = 0
# ------------------------------
# Função para criar e preencher tabelas
# ------------------------------
def create_table_from_matrix(frame, matrix, height=5):
    """
    matrix: lista de listas de strings
    A primeira linha da matrix é o cabeçalho (nomes das colunas)
    As demais linhas são os dados
    """

    columns = matrix[0]

    table = ttk.Treeview(frame, columns=columns, show="headings", height=height)

    # Criar colunas
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100, anchor="center")

    table.pack(fill="x", pady=5)

    # Inserir dados da matriz
    for row in matrix[1:]:
        table.insert("", "end", values=row)

    return table

# ------------------------------
# Função para limpar widgets
# ------------------------------
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# ------------------------------
# Função chamada pelo botão "Próximo"
# ------------------------------
def proximo():
    global index, status_frame, rob_frame, uf_frame, ls_frame, reg_frame

    clock_label.config(
        text=f"Clock: {index} | IPC: {toma.IIpc[index]} | Bolhas: {toma.bobolhas[index]}"
    )


    # limitar ao tamanho do simulador
    if index < len(toma.geral) - 1:
        index += 1

    # atualizar clock
    #clock_label.config(text=f"Clock: {index}")

    # RECRIAR TODAS AS TABELAS
    clear_frame(status_frame)
    clear_frame(rob_frame)
    clear_frame(uf_frame)
    #clear_frame(ls_frame)
    clear_frame(reg_frame)

    # NOVAS MATRIZES
    status_instr_matrix = toma.status_das_instrucoes[index]
    rob_matrix = toma.buff[index]
    uf_matrix = toma.UniFunc[index]
    reg_matrix = toma.regregis[index]
    

    # você pode substituir essas por matrizes reais depois
    create_table_from_matrix(status_frame, status_instr_matrix)
    create_table_from_matrix(rob_frame, rob_matrix)
    create_table_from_matrix(uf_frame, uf_matrix)
    #create_table_from_matrix(ls_frame, ls_matrix)
    create_table_from_matrix(reg_frame, reg_matrix, height=2)


def anterior():
    global index, status_frame, rob_frame, uf_frame, ls_frame, reg_frame

    clock_label.config(
        text=f"Clock: {index} | IPC: {toma.IIpc[index]} | Bolhas: {toma.bobolhas[index]}"
    )


    # limitar ao tamanho do simulador
    if index < len(toma.geral) - 1:
        index -= 1

    # atualizar clock
    #clock_label.config(text=f"Clock: {index}")

    # RECRIAR TODAS AS TABELAS
    clear_frame(status_frame)
    clear_frame(rob_frame)
    clear_frame(uf_frame)
    #clear_frame(ls_frame)
    clear_frame(reg_frame)

    # NOVAS MATRIZES
    status_instr_matrix = toma.status_das_instrucoes[index]
    rob_matrix = toma.buff[index]
    uf_matrix = toma.UniFunc[index]
    reg_matrix = toma.regregis[index]
    

    # você pode substituir essas por matrizes reais depois
    create_table_from_matrix(status_frame, status_instr_matrix)
    create_table_from_matrix(rob_frame, rob_matrix)
    create_table_from_matrix(uf_frame, uf_matrix)
    #create_table_from_matrix(ls_frame, ls_matrix)
    create_table_from_matrix(reg_frame, reg_matrix, height=2)


# ------------------------------
# INTERFACE PRINCIPAL
# ------------------------------
root = tk.Tk()
root.title("Simulador Tomasulo - Interface com Matrizes")

main = ttk.Frame(root, padding=10)
main.pack(fill="both", expand=True)


# -----------------------------------
# Top: Botões
# -----------------------------------
top_frame = ttk.Frame(main)
top_frame.pack(fill="x", pady=10)

ttk.Button(top_frame, text="← Voltar", command=anterior).pack(side="left")
ttk.Button(top_frame, text="Próximo ➜", command=proximo).pack(side="left")

ipc = toma.IIpc
bolhas = toma.bobolhas

clock_label = ttk.Label(
    top_frame,
    text=f"Clock: {index} | IPC: {ipc[index]} | Bolhas: {0}",
    relief="solid",
    padding=5
)
clock_label.pack(side="right")




# ============================================================
#                   MATRIZES DAS TABELAS
# ============================================================

status_instr_matrix = toma.status_das_instrucoes[index]

rob_matrix = toma.buff[index]
'''[
    ["Entrada", "Ocupado", "Instrução", "Estado", "Destino", "Valor"],
    ["0", "não", "LD F2, 0, R1", "Issue", "-", "-"],
    ["1", "não", "ADDD F4, F6, F2", "Issue", "-", "-"],
    ["2", "não", "DIVD F2, F6, F6", "Issue", "-", "-"],
    ["3", "não", "MULTD F10, F2, F4", "Issue", "-", "-"],
    ["4", "não", "SUBD F4, F8, F8", "Issue", "-", "-"]
]'''

uf_matrix = toma.UniFunc[index]
'''[
    ["Tempo", "UF", "Ocupado", "Op", "Vj", "Vk", "Qj", "Qk"],
    ["", "Integer1", "não", "", "", "", "", ""],
    ["", "Integer2", "não", "", "", "", "", ""],
    ["", "Add1", "não", "", "", "", "", ""],
    ["", "Add2", "não", "", "", "", "", ""],
    ["", "Mult1", "não", "", "", "", "", ""]
]'''

ls_matrix = [
    ["Tempo", "Instrução", "Ocupado", "Endereço", "Destino"],
    ["", "Load1", "não", "", ""],
    ["", "Load2", "não", "", ""],
    ["", "Store1", "não", "", ""]
]

reg_matrix = toma.regregis[index]
'''[
    ["F0","F2","F4","F6","F8","F10","F12","F14","F16","F18","F20","F22","F24","F26","F28","F30"],
    ["F2","F4","F6","F8","F10","F12","F14","F16","F18","F20","F22","F24","F26","F28","F30",""]
]'''


# ============================================================
#               CRIAÇÃO DAS TABELAS A PARTIR DAS MATRIZES
# ============================================================

# STATUS DAS INSTRUÇÕES
status_frame = ttk.LabelFrame(main, text="Status das instruções")
status_frame.pack(fill="x", pady=10)
create_table_from_matrix(status_frame, status_instr_matrix)

# ROB
rob_frame = ttk.LabelFrame(main, text="Buffer de Reordenamento")
rob_frame.pack(fill="x", pady=10)
create_table_from_matrix(rob_frame, rob_matrix)

# UF
uf_frame = ttk.LabelFrame(main, text="Unidades Funcionais")
uf_frame.pack(fill="x", pady=10)
create_table_from_matrix(uf_frame, uf_matrix)

# LOAD / STORE
ls_frame = ttk.LabelFrame(main, text="Unidades Funcionais Load/Store")
ls_frame.pack(fill="x", pady=10)
#create_table_from_matrix(ls_frame, ls_matrix)

# REGISTRADORES
reg_frame = ttk.LabelFrame(main, text="Estado dos registradores")
reg_frame.pack(fill="x", pady=10)
create_table_from_matrix(reg_frame, reg_matrix, height=2)


# -----------------------------------
# Inicia GUI
# -----------------------------------
root.mainloop()
