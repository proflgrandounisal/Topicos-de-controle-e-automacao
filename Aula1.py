import matplotlib.pyplot as plt
import numpy as np
import time

# ==============================================================================
# 1. PLANTA E LÓGICA (MANTIDAS)
# ==============================================================================
class PlantaTanque:
    def __init__(self, vazamento_inicial):
        self.y = 0.0  
        self.d = vazamento_inicial 
        self.capacidade = 100.0

    def transicao_estado(self, u):
        vazao_bomba = u * 0.5 
        saida = self.d
        self.y += (vazao_bomba - saida)
        self.y = max(0.0, min(self.capacidade, self.y))
        return self.y, vazao_bomba

# ==============================================================================
# 2. INPUTS (HMI)
# ==============================================================================
print("\n=== 🏭 CONFIGURAÇÃO DE CONTROLE FIXO ===")
r = float(input("Setpoint [r] (0-100 cm) [Padrão 70]: ") or 70)
kp = float(input("Ganho [Kp] [Padrão 3.0]: ") or 3.0)
d_ini = float(input("Vazamento Inicial (L/s) [Padrão 2.0]: ") or 2.0)
t_dist = int(input("Tempo do Incidente (s) [Padrão 50]: ") or 50)
d_fim = float(input("Novo Vazamento (L/s) [Padrão 5.0]: ") or 5.0)
t_total = int(input("Tempo Total [Padrão 100]: ") or 100)

# ==============================================================================
# 3. SETUP DOS GRÁFICOS (FIXOS)
# ==============================================================================
tanque_ma = PlantaTanque(d_ini)
tanque_mf = PlantaTanque(d_ini)

t_eixo, sp_eixo = [], []
ma_y, mf_y = [], []
ma_vazao, mf_vazao = [], []

# Criar a figura e os eixos
plt.close('all') # Fecha janelas fantasmas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
plt.subplots_adjust(hspace=0.3)

# Configuração do Gráfico de Nível (PV)
ax1.set_xlim(0, t_total)
ax1.set_ylim(-5, 110)
ax1.set_ylabel("Nível y(t) [cm]")
ax1.grid(True, alpha=0.3)
line_sp, = ax1.plot([], [], 'k--', label='Setpoint r(t)')
line_ma_y, = ax1.plot([], [], 'r-', label='Nível (Malha Aberta)', alpha=0.5)
line_mf_y, = ax1.plot([], [], 'g-', label='Nível (Malha Fechada)', linewidth=2)
ax1.legend(loc='upper left')

# Configuração do Gráfico de Vazão (MV)
ax2.set_xlim(0, t_total)
ax2.set_ylim(-1, 15) # Escala para vazão
ax2.set_ylabel("Vazão u(t) [L/s]")
ax2.set_xlabel("Tempo (s)")
ax2.grid(True, alpha=0.3)
line_ma_u, = ax2.plot([], [], 'r-', label='Vazão (Aberta)', alpha=0.5)
line_mf_u, = ax2.plot([], [], 'g-', label='Vazão (Fechada)', linewidth=2)
ax2.legend(loc='upper left')

# Linha de perturbação (inicia oculta)
vline1 = ax1.axvline(x=t_dist, color='orange', linestyle=':', alpha=0)
vline2 = ax2.axvline(x=t_dist, color='orange', linestyle=':', alpha=0)

plt.show(block=False) # Mostra a janela sem travar o script

# ==============================================================================
# 4. LOOP DE EXECUÇÃO (FRAME POR FRAME)
# ==============================================================================
for t in range(t_total):
    if t == t_dist:
        tanque_ma.d = d_fim
        tanque_mf.d = d_fim
        vline1.set_alpha(1) # Mostra a linha no tempo exato
        vline2.set_alpha(1)

    # Malha Aberta
    u_ma = d_ini / 0.5 
    y_ma, v_ma = tanque_ma.transicao_estado(u_ma)

    # Malha Fechada
    erro = r - tanque_mf.y
    u_mf = kp * erro
    u_mf = max(0, min(100, u_mf)) 
    y_mf, v_mf = tanque_mf.transicao_estado(u_mf)

    # Coleta de Dados
    t_eixo.append(t)
    sp_eixo.append(r)
    ma_y.append(y_ma); mf_y.append(y_mf)
    ma_vazao.append(v_ma); mf_vazao.append(v_mf)

    # ATUALIZAÇÃO DOS GRÁFICOS (Sem redesenhar o eixo)
    line_sp.set_data(t_eixo, sp_eixo)
    line_ma_y.set_data(t_eixo, ma_y)
    line_mf_y.set_data(t_eixo, mf_y)
    
    line_ma_u.set_data(t_eixo, ma_vazao)
    line_mf_u.set_data(t_eixo, mf_vazao)
    
    # Refresh da interface
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.05) # Estabilidade da animação

print("\n🏁 Simulação concluída com sucesso.")
plt.show(block=True) # Mantém o gráfico aberto no final
