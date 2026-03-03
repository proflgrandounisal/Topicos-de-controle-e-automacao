"""
Disciplina: Tópicos de Controle e Automação
Projeto: SmartFlow - Sprint 1 (Modelagem e Arquitetura)
Script: aula3_modelagem.py

Objetivo:
Demonstrar a implementação de um Diagrama de Blocos em software.
Cada componente do sistema real é abstraído como uma classe isolada.
A Planta utiliza a Equação de Diferenças para simular o tempo discreto.
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. DEFINIÇÃO DOS BLOCOS DA ARQUITETURA
# =============================================================================

class Planta:
    """
    O Fenômeno Físico (Núcleo do TCC / Tanque SmartFlow).
    Obedece às leis da conservação de massa.
    """
    def __init__(self, area_tanque, nivel_inicial):
        self.A = area_tanque
        self.h = nivel_inicial
        self.q_out_base = 0.0 # Perturbação natural

    def atualizar_estado(self, q_in, q_out_extra, dt):
        """
        Equação de Diferenças: h[k+1] = h[k] + ((Qin - Qout) * dt) / A
        """
        q_out_total = self.q_out_base + q_out_extra
        
        # O modelo matemático em tempo discreto
        self.h = self.h + ((q_in - q_out_total) * dt) / self.A
        
        # Limite físico: o tanque não pode ter nível negativo
        if self.h < 0.0:
            self.h = 0.0
            
        return self.h

class Sensor:
    """
    Traduz a grandeza física (PV) para o algoritmo.
    Pode incluir atrasos, quantização ou ruído (conforme Aula 2).
    """
    def ler_variavel(self, valor_real):
        # Aqui assumimos um sensor ideal para focar na modelagem arquitetural.
        # Alunos podem herdar esta classe e adicionar ruído para seus TCCs.
        return valor_real

class Atuador:
    """
    Converte o comando lógico (0 a 100%) em ação física (Vazão em L/s).
    """
    def __init__(self, capacidade_maxima):
        self.q_max = capacidade_maxima

    def acionar(self, sinal_controle):
        # Saturador: O controle lógico não pode exigir mais que 100% ou menos que 0%
        sinal_saturado = max(0.0, min(100.0, sinal_controle))
        # Conversão linear de % para Litros/segundo
        vazao_fisica = (sinal_saturado / 100.0) * self.q_max
        return vazao_fisica

class Controlador:
    """
    O Cérebro (Equivalente ao microcontrolador ou CLP).
    Calcula o Erro e define o esforço de controle.
    """
    def __init__(self, kp):
        self.kp = kp

    def calcular_comando(self, setpoint, pv):
        # O Ponto de Soma do Diagrama de Blocos
        erro = setpoint - pv
        # Ganho Proporcional Simples (O PID completo será na Sprint 2)
        comando = self.kp * erro
        return comando

# =============================================================================
# 2. CONFIGURAÇÃO DA SIMULAÇÃO (O GÊMEO DIGITAL)
# =============================================================================

# Parâmetros de Tempo
TEMPO_TOTAL = 100       # Segundos
DT = 1.0                # Tempo de amostragem (Passo discreto)
passos = int(TEMPO_TOTAL / DT)

# Instanciando a Arquitetura
tanque = Planta(area_tanque=2.5, nivel_inicial=10.0)
sensor_nivel = Sensor()
bomba = Atuador(capacidade_maxima=5.0) # Bomba injeta no máximo 5 L/s
algoritmo = Controlador(kp=8.0)

# Parâmetros de Operação
SP = 50.0 # Queremos estabilizar o tanque em 50 Litros

# Histórico para plotagem
log_tempo = []
log_sp = []
log_pv = []
log_mv = []

# =============================================================================
# 3. LOOP PRINCIPAL (TEMPO DISCRETO)
# =============================================================================

print("Iniciando simulação da malha fechada...")

for k in range(passos):
    tempo_atual = k * DT
    
    # Inserindo uma Perturbação Externa (Distúrbio) no segundo 40
    # Simula um vazamento abrupto no sistema
    vazamento = 2.0 if tempo_atual >= 40 else 0.0

    # Passo 1: Leitura do Sensor (PV)
    pv_atual = sensor_nivel.ler_variavel(tanque.h)
    
    # Passo 2: Cálculo do Controlador
    sinal_u = algoritmo.calcular_comando(SP, pv_atual)
    
    # Passo 3: Ação do Atuador (Converte lógico para físico)
    vazao_entrada = bomba.acionar(sinal_u)
    
    # Passo 4: Atualização da Planta (A Física reage)
    tanque.atualizar_estado(vazao_entrada, vazamento, DT)

    # Registro de Dados
    log_tempo.append(tempo_atual)
    log_sp.append(SP)
    log_pv.append(pv_atual)
    log_mv.append(sinal_u)

# =============================================================================
# 4. VISUALIZAÇÃO GRÁFICA (MATPLOTLIB)
# =============================================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Gráfico Superior: Variável de Processo vs Setpoint
ax1.plot(log_tempo, log_sp, 'r--', label='Setpoint (SP) = 50L', linewidth=2)
ax1.plot(log_tempo, log_pv, 'b-', label='Variável de Processo (PV)', linewidth=2)
ax1.axvline(x=40, color='gray', linestyle=':', label='Perturbação (Vazamento)')
ax1.set_title("Comportamento do Sistema - Modelagem Discreta")
ax1.set_ylabel("Nível (Litros)")
ax1.legend(loc='lower right')
ax1.grid(True)

# Gráfico Inferior: Variável Manipulada (Sinal de Controle)
ax2.plot(log_tempo, log_mv, 'g-', label='Comando do Controlador (U)', linewidth=2)
ax2.axvline(x=40, color='gray', linestyle=':')
ax2.set_ylabel("Esforço (%)")
ax2.set_xlabel("Tempo (segundos)")
ax2.set_ylim(-10, 110) # Limites de 0 a 100% de saturação
ax2.legend(loc='upper right')
ax2.grid(True)

plt.tight_layout()
plt.show()
