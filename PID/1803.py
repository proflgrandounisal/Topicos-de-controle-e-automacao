import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# PLANTA FÍSICA (GÊMEO DIGITAL)
# ==============================================================================
def planta_aquecedor(T_atual, U_atual, ruido_amp, dt):
    """
    Simulação de um sistema térmico de 1ª ordem.
    Equação Contínua: G(s) = K / (tau*s + 1)
    """
    tau = 20.0  # Constante de tempo (Inércia Térmica)
    K = 1.0     # Ganho estático (Para 100% de PWM, sobe 100 graus teóricos)
    
    ruido = np.random.uniform(-ruido_amp, ruido_amp)
    
    # Discretização explícita (Euler) da equação diferencial
    T_nova = T_atual + (dt / tau) * (K * U_atual - T_atual) + ruido
    return T_nova

# ==============================================================================
# ALGORITMOS DE CONTROLE
# ==============================================================================
def simular_controle(modo, Kp=0, Ki=0, Kd=0, histerese=0, ruido_amp=0.5):
    passos = 150
    dt = 1.0  # Tempo de amostragem explícito (Conecta com a integral/derivada real)
    SP = 50.0
    
    T = np.zeros(passos)
    U = np.zeros(passos)
    Erro_hist = np.zeros(passos)
    
    T[0] = 20.0
    integral = 0.0
    erro_anterior = SP - T[0]
    
    for k in range(1, passos):
        T_anterior = T[k-1]
        
        # 1. Leitura do Sensor e Cálculo do Erro
        erro = SP - T_anterior
        Erro_hist[k] = erro
        
        # 2. Lógica do Controlador
        if modo == 'ON/OFF':
            U[k] = 100.0 if T_anterior < SP else 0.0
            
        elif modo == 'HISTERESE':
            # Decisão baseada diretamente na PV vs SP (Evita confusão conceitual)
            if T_anterior < (SP - histerese):
                U[k] = 100.0
            elif T_anterior > (SP + histerese):
                U[k] = 0.0
            else:
                U[k] = U[k-1] # Retenção de estado
                
        elif modo in ['PID', 'PID_CAOS']:
            # A Matemática Pura (Tempo Discreto)
            integral += erro * dt
            derivada = (erro - erro_anterior) / dt
            
            # O que a matemática pede (Pode pedir infinito)
            U_raw = (Kp * erro) + (Ki * integral) + (Kd * derivada)
            
            # O que o mundo físico aceita (Saturação 0 a 100%)
            U[k] = max(0.0, min(100.0, U_raw))
            
            # Anti-Windup (O grampo algorítmico)
            if U_raw > 100.0 or U_raw < 0.0:
                integral -= erro * dt # Desfaz o acúmulo irreal
                
            erro_anterior = erro
            
        # 3. Atualização da Planta Física
        T[k] = planta_aquecedor(T[k-1], U[k], ruido_amp, dt)
        
    return T, U, Erro_hist

# ==============================================================================
# PLOTAGEM DO LABORATÓRIO (COMPARATIVO SOCRÁTICO)
# ==============================================================================
modos = [
    {'nome': '1. ON/OFF (O Chattering e a Destruição do Atuador)', 'tipo': 'ON/OFF', 'params': {}},
    {'nome': '2. Histerese (Protege Hardware, mas mantém a oscilação)', 'tipo': 'HISTERESE', 'params': {'histerese': 3.0}},
    {'nome': '3. Somente [P] (O Erro de Regime Permanente)', 'tipo': 'PID', 'params': {'Kp': 4.0, 'Ki': 0.0, 'Kd': 0.0}},
    {'nome': '4. [P] + [I] (Elimina o erro, mas gera Overshoot)', 'tipo': 'PID', 'params': {'Kp': 4.0, 'Ki': 0.8, 'Kd': 0.0}},
    {'nome': '5. [P] + [I] + [D] (O Freio Preditivo - Sintonia Ideal)', 'tipo': 'PID', 'params': {'Kp': 4.0, 'Ki': 0.8, 'Kd': 6.0}},
    {'nome': '6. O Perigo do [D] (Derivada Amplificando Ruído -> CAOS)', 'tipo': 'PID_CAOS', 'params': {'Kp': 4.0, 'Ki': 0.8, 'Kd': 15.0, 'ruido_amp': 4.0}}
]

fig, axs = plt.subplots(len(modos), 1, figsize=(12, 18), sharex=True)
fig.suptitle('Laboratório de Controle: Causalidade Dinâmica em Tempo Real', fontsize=16, fontweight='bold')

t = np.arange(150)
SP = 50.0

for i, config in enumerate(modos):
    T_sim, U_sim, E_sim = simular_controle(config['tipo'], **config['params'])
    
    # Eixo principal (Variáveis de Processo e Erro)
    axs[i].plot(t, T_sim, label='PV (Temperatura)', color='#1f77b4', lw=2)
    axs[i].plot(t, E_sim + SP, label='Erro Relativo (E)', color='purple', linestyle='-.', lw=1.5, alpha=0.6)
    axs[i].axhline(SP, color='red', linestyle='--', label='Setpoint (SP)', alpha=0.8)
    
    if config['tipo'] == 'HISTERESE':
        axs[i].axhline(SP + config['params']['histerese'], color='orange', linestyle=':', alpha=0.5)
        axs[i].axhline(SP - config['params']['histerese'], color='orange', linestyle=':', alpha=0.5)

    axs[i].set_title(config['nome'], fontsize=11, loc='left', color='black', fontweight='bold')
    axs[i].set_ylabel('°C / Erro', fontsize=10)
    axs[i].grid(True, linestyle=':', alpha=0.6)
    
    # Eixo secundário (Variável Manipulada)
    ax_u = axs[i].twinx()
    ax_u.fill_between(t, 0, U_sim, color='green', alpha=0.2, step='post')
    ax_u.step(t, U_sim, color='green', alpha=0.6, where='post', lw=1.5, label='MV (Atuador %)')
    ax_u.set_ylabel('Motor %', color='green', fontsize=10)
    ax_u.set_ylim(-5, 105)

    if i == 0: # Legenda apenas no primeiro gráfico para não poluir
        linhas_1, labels_1 = axs[i].get_legend_handles_labels()
        linhas_2, labels_2 = ax_u.get_legend_handles_labels()
        axs[i].legend(linhas_1 + linhas_2, labels_1 + labels_2, loc='lower right', ncol=4, fontsize=9)

plt.xlabel('Tempo Discreto [k] (Amostras)', fontsize=12)
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()
