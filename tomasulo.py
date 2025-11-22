class Instrucao:
    

    def __init__(self, nome, i, j, k, issue, exec_completa, write_result, tipo, vida):
        self.nome = nome
        self.i = i
        self.j = j
        self.k = k
        self.issue = issue
        self.exec_completa = exec_completa
        self.write_result = write_result
        self.tipo = tipo
        self.vida = vida

    def __str__(self):
        return (f"Instrução: {self.nome}, i: {self.i}, j: {self.j}, k: {self.k}, "
            f"Issue: {self.issue if self.issue is not None else 'N/A'}, "
            f"Exec. Completa: {self.exec_completa if self.exec_completa is not None else 'N/A'}, "
            f"Write Result: {self.write_result if self.write_result is not None else 'N/A'}")
    
    def to_dict(self):
        """
        Retorna a instrução como um dicionário.
        """
        return {
            "Instrução": self.nome,
            "i": self.i,
            "j": self.j,
            "k": self.k,
            "Issue": self.issue,
            "Exec. Completa": self.exec_completa,
            "Write Result": self.write_result
        }

class Unidades_Funcionais:
    def __init__(self, nome, tempo, instrucao, Ocupado, vida):
        self.nome = nome
        self.tempo = tempo
        self.instrucao = instrucao
        self.Ocupado = Ocupado
        #self.id = id
        self.vida = vida
        #self.qtd = qtd
    def _start_(self, nome, tempo, Ocupado):
        self.nome = nome
        self.tempo = tempo
        self.Ocupado = Ocupado


class Tomasulo:
    TEMPO_EXECUCAO = {
        "ADD": 2,    # Adição/Subtração/Lógica
        "SUB": 2,
        "MULT": 10,  # Multiplicação
        "DIV": 40,   # Divisão
        "LOAD": 2,   # Load (Acesso à memória)
        "STORE": 2,  # Store (Acesso à memória)
        "BEQ": 3     # Branch Equal (Salto condicional)
        # Assuma que a instrução "end" é ignorada na execução
    }

    def ler_arquivo(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
            return conteudo
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao ler o arquivo: {e}")
            return None
        
    def decodificar_instrucoes(self, conteudo_instrucoes):

        instrucoes_decodificadas = []
        
        if not conteudo_instrucoes:
            print("Conteúdo das instruções está vazio.")
            return instrucoes_decodificadas

        # Divide o conteúdo em linhas
        linhas = conteudo_instrucoes.strip().split('\n')
        
        for linha in linhas:
            # Remove espaços em branco e verifica se a linha não está vazia
            linha_limpa = linha.strip()
            if not linha_limpa or linha_limpa.lower() == 'end':
                # Ignora linhas vazias e a instrução 'end'
                continue

            # Divide a linha pelos delimitadores (vírgula e espaço)
            partes = [p.strip() for p in linha_limpa.split(',')]
            
            # Garante que temos pelo menos 4 partes (NOME, i, j, k)
            if len(partes) < 4:
                print(f"Aviso: Linha de instrução ignorada por formato inválido: {linha_limpa}")
                continue

            nome = partes[0]
            i = partes[1]
            j = partes[2]
            k = partes[3]

            ty = ""
            if nome == "ADD" or nome == "SUB":
                ty = "ALU"
            elif nome == "MULT" or nome == "DIV":
                ty = "MULT"
            elif nome == "BEQ" or nome == "BNE":
                ty = "BR"
            elif nome == "LD" or nome == "SD":
                ty = "MEM"

            # Cria a instância da Instrucao. Os campos de ciclo (para a simulação de Tomasulo)
            # são inicializados como None, pois serão preenchidos durante a execução.
            instrucao = Instrucao(
                nome=nome,
                i=i,
                j=j,
                k=k,
                issue= -1,          # Será definido quando a instrução for emitida
                exec_completa= -1,  # Será definido quando a execução terminar
                write_result= -1,   # Será definido quando o resultado for escrito
                tipo= ty,
                vida= 0
            )
            
            instrucoes_decodificadas.append(instrucao)
            
        return instrucoes_decodificadas
    
    def despacho(self, ufs, erALU, erMULT,erMEM, erBR):
        for u in ufs:
            if u.Ocupado == False and u.nome == "ALU" and len(erALU) > 0:
                u.instrucao = erALU.pop(0)
                u.Ocupado = True
                u.vida = 0

            if u.Ocupado == False and u.nome == "MULT" and len(erMULT) > 0:
                u.instrucao = erMULT.pop(0)
                u.Ocupado = True
                u.vida = 0

            if u.Ocupado == False and u.nome == "MEM" and len(erMEM) > 0:
                u.instrucao = erMEM.pop(0)
                u.Ocupado = True
                u.vida = 0

            if u.Ocupado == False and u.nome == "BR" and len(erBR) > 0:
                u.instrucao = erBR.pop(0)
                u.Ocupado = True
                u.vida = 0
          
    def atualiza_clock(self, ufs, clock):
        tmpInst = Instrucao(0,0,0,0,0,0,0,0,0)
        for u in ufs:
            if u.Ocupado == True and u.instrucao.exec_completa == -1:
                if u.tempo == u.vida:
                    u.Ocupado = False
                    u.vida = 0
                    u.instrucao.exec_completa = clock
                    u.instrucao = tmpInst
                else:
                    u.vida = u.vida + 1
                    #u.instrucao.exec_completa = 10
    
    def atualizar_inst(self, instrucoes, clock):
        for instr in instrucoes:
            if instr.exec_completa > -1 & instr.write_result == -1:
                instr.write_result = clock

    def imprimir_tabela(self, instrucoes):
        print(f"{'Nome':<8} {'i':<3} {'j':<3} {'k':<3} {'Issue':<6} {'Exec':<6} {'Write':<6} {'Tipo':<6} {'Vida':<4}")
        print("-" * 60)

        for inst in instrucoes:
            print(f"{inst.nome:<8} {inst.i:<3} {inst.j:<3} {inst.k:<3} "
                f"{inst.issue:<6} {inst.exec_completa:<6} {inst.write_result:<6} "
                f"{inst.tipo:<6} {inst.vida:<4}")

    def simulador(self):
        
        #er = EstacaoDeReserva()
        clock = 0

        caminho = './instruct.luix'
        conteudo = self.ler_arquivo(caminho)
        instrucoes = self.decodificar_instrucoes(conteudo)

        # Estacoes de reserva
        erALU = []
        erMULT = []
        erMEM = []
        erBR = []

        # unidades funcionais
        ufs = [] 
        tmpInst = Instrucao(0,0,0,0,0,0,0,0,0) # TMP apenas para formato

        ufALU_1 = Unidades_Funcionais('ALU', 2, tmpInst, False, 0)
        #ufALU_1._start_("ALU", 2, False)
        ufALU_2 = Unidades_Funcionais('ALU', 2, tmpInst, False, 0)
        #ufALU_2._start_("ALU", 2, False)

        ufMULT = Unidades_Funcionais('MULT', 6, tmpInst, False, 0)
        #ufMULT._start_("MULT", 6, False)

        ufMEM = Unidades_Funcionais('MEM', 4, tmpInst, False, 0)
        #ufMEM._start_("MEM", 4, False)

        ufBR = Unidades_Funcionais('BR', 1, tmpInst, False, 0)
        #ufBR._start_("BR", 1, False)

        ufs = [ufALU_1, ufALU_2, ufMULT, ufMEM, ufBR]
        
        

        # ---- Tomasulu ---- # loop
        while instrucoes[-1].write_result < 0:
            for i in range(clock*2, 2 + clock*2):          # Instuçoes sao carregadas nas estacoes
                if i < len(instrucoes):
                    inst = instrucoes[i]
                    if inst.tipo == "ALU":
                        inst.issue = clock
                        erALU.append(inst)
                    elif inst.tipo == "MULT":
                        inst.issue = clock
                        erMULT.append(inst)
                    elif inst.tipo == "MEM":
                        inst.issue = clock
                        erMEM.append(inst)
                    elif inst.tipo == "BR":
                        inst.issue = clock
                        erBR.append(inst)
        
            # Despacho de instrucao
            self.despacho(ufs, erALU, erMULT,erMEM, erBR)
            self.atualiza_clock(ufs, clock)
            self.atualizar_inst(instrucoes, clock)

            print("---------------------------------------")
            print(clock)
            self.imprimir_tabela(instrucoes)
            clock = clock + 1
            #print(ufs[0].instrucao.exec_completa)
        #print(instrucoes[-1].write_result)



        # ---- Tomasulu ---- # loop

t = Tomasulo()
t.simulador()
