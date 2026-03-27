import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# =============================================================================
# 1. SETUP DO CONTROLADOR FUZZY
# =============================================================================
universo_erro = np.arange(-50, 51, 1)
universo_derro = np.arange(-10, 11, 1)
universo_bomba = np.arange(0, 101, 1)

erro = ctrl.Antecedent(universo_erro, 'erro')
derro = ctrl.Antecedent(universo_derro, 'derro')
bomba = ctrl.Consequent(universo_bomba, 'bomba')

# Salvando as funções (mf) em variáveis para podermos extrair a matemática depois
mf_erro_neg = fuzz.trapmf(universo_erro, [-50, -50, -5, 0])
mf_erro_zer = fuzz.trimf(universo_erro, [-5, 0, 5])
mf_erro_pos = fuzz.trapmf(universo_erro, [0, 5, 50, 50])

mf_derro_cai = fuzz.trapmf(universo_derro, [-10, -10, -2, 0])
mf_derro_est = fuzz.trimf(universo_derro, [-2, 0, 2])
mf_derro_sub = fuzz.trapmf(universo_derro, [0, 2, 10, 10])

erro['negativo'] = mf_erro_neg
erro['zero']     = mf_erro_zer
erro['positivo'] = mf_erro_pos

derro['caindo']  = mf_derro_cai
derro['estavel'] = mf_derro_est
derro['subindo'] = mf_derro_sub

bomba['desligada']  = fuzz.trimf(universo_bomba, [0, 0, 10])
bomba['manutencao'] = fuzz.trimf(universo_bomba, [10, 30, 50])
bomba['forte']      = fuzz.trapmf(universo_bomba, [40, 60, 100, 100])

# =============================================================================
# BASE DE REGRAS ROBUSTA (Matriz Completa para evitar Limbo Lógico)
# =============================================================================

# ZONA 1: Quando o nível está ABAIXO do alvo (Erro Positivo)
regra1 = ctrl.Rule(erro['positivo'] & derro['subindo'], bomba['forte'])  # Esvaziando? Força total!
regra2 = ctrl.Rule(erro['positivo'] & derro['estavel'], bomba['forte'])  # Parado abaixo do alvo? Força total!
regra3 = ctrl.Rule(erro['positivo'] & derro['caindo'], bomba['forte'])   # Enchendo? Mantém força total.

# ZONA 2: Quando o nível está NA ZONA DO ALVO (Erro Zero)
regra4 = ctrl.Rule(erro['zero'] & derro['subindo'], bomba['forte'])      # Começou a vazar e cair? Acelera!
regra5 = ctrl.Rule(erro['zero'] & derro['estavel'], bomba['manutencao']) # Estabilizou no alvo? Mantém a bomba em 30% a 40%!
regra6 = ctrl.Rule(erro['zero'] & derro['caindo'], bomba['desligada'])   # Chegou no alvo rápido demais? Desliga pra frear o Overshoot.

# ZONA 3: Quando o nível PASSOU do alvo (Erro Negativo)
regra7 = ctrl.Rule(erro['negativo'], bomba['desligada'])                 # Passou do limite? Corta tudo.

sistema_fuzzy = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7])

# flush_after_run=1 limpa a memória entre iterações do loop no Modo 1 para evitar acúmulo
simulador_fuzzy = ctrl.ControlSystemSimulation(sistema_fuzzy, flush_after_run=1)

SP = 30.0  # Setpoint (Alvo)

# =============================================================================
# 2. MOTOR DE FEEDBACK MATEMÁTICO (Para o Modo Interativo)
# =============================================================================
def imprimir_matematica_fuzzy(valor_erro, valor_derro, valor_pwm):
    print("\n" + "-"*50)
    print(" ANÁLISE INTERNA: MOTOR DE INFERÊNCIA FUZZY")
    print("-"*50)
    
    # Calculando os graus de pertinência exatos
    g_e_neg = fuzz.interp_membership(universo_erro, mf_erro_neg, valor_erro)
    g_e_zer = fuzz.interp_membership(universo_erro, mf_erro_zer, valor_erro)
    g_e_pos = fuzz.interp_membership(universo_erro, mf_erro_pos, valor_erro)
    
    g_d_cai = fuzz.interp_membership(universo_derro, mf_derro_cai, valor_derro)
    g_d_est = fuzz.interp_membership(universo_derro, mf_derro_est, valor_derro)
    g_d_sub = fuzz.interp_membership(universo_derro, mf_derro_sub, valor_derro)
    
    print(f"1. Fuzzificação do Erro ({valor_erro:.1f} Litros):")
    print(f"   -> Negativo (Passou): {g_e_neg:.2f} | Zero (No alvo): {g_e_zer:.2f} | Positivo (Falta): {g_e_pos:.2f}")
    
    print(f"\n2. Fuzzificação da Variação ({valor_derro:.1f} L/s):")
    print(f"   -> Caindo: {g_d_cai:.2f} | Estável: {g_d_est:.2f} | Subindo: {g_d_sub:.2f}")
    
    print("\n3. Defuzzificação (Centro de Gravidade):")
    print(f"   >>> SINAL ENVIADO PARA A BOMBA: {valor_pwm:.1f}% <<<")
    print("-"*50)

# =============================================================================
# 3. PLANTA FÍSICA E SIMULAÇÃO COMPLETA
# =============================================================================
def planta_tanque(nivel_atual, pwm_bomba, dt):
    vazao_maxima = 2.0  
    coef_vazamento = 0.05 
    entrada = (pwm_bomba / 100.0) * vazao_maxima
    saida = coef_vazamento * nivel_atual
    return max(0.0, nivel_atual + (entrada - saida) * dt)

def executar_simulacao_completa():
    passos = 150
    dt = 1.0
    t = np.arange(passos)
    h_onoff, u_onoff = np.zeros(passos), np.zeros(passos)
    h_pid, u_pid = np.zeros(passos), np.zeros(passos)
    h_fuzzy, u_fuzzy = np.zeros(passos), np.zeros(passos)

    Kp, Ki, Kd = 2.5, 0.4, 1.5
    integral, erro_ant_pid, erro_ant_fuz = 0.0, 0.0, 0.0

    print("\nExecutando simulação de 150 segundos. Aguarde os gráficos...")

    for k in range(1, passos):
        # ON/OFF
        if h_onoff[k-1] < SP - 2: u_onoff[k] = 100.0
        elif h_onoff[k-1] > SP + 2: u_onoff[k] = 0.0
        else: u_onoff[k] = u_onoff[k-1]
        h_onoff[k] = planta_tanque(h_onoff[k-1], u_onoff[k], dt)

        # PID
        erro_pid = SP - h_pid[k-1]
        integral += erro_pid * dt
        derivada = (erro_pid - erro_ant_pid) / dt
        u_raw = (Kp * erro_pid) + (Ki * integral) + (Kd * derivada)
        u_pid[k] = max(0.0, min(100.0, u_raw))
        if u_raw > 100.0 or u_raw < 0.0: integral -= erro_pid * dt
        erro_ant_pid = erro_pid
        h_pid[k] = planta_tanque(h_pid[k-1], u_pid[k], dt)

        # FUZZY
        erro_fuz = SP - h_fuzzy[k-1]
        derro_fuz = (erro_fuz - erro_ant_fuz) / dt
        simulador_fuzzy.input['erro'] = max(-50, min(50, erro_fuz))
        simulador_fuzzy.input['derro'] = max(-10, min(10, derro_fuz))
        simulador_fuzzy.compute()
        u_fuzzy[k] = max(0.0, min(100.0, simulador_fuzzy.output['bomba']))
        erro_ant_fuz = erro_fuz
        h_fuzzy[k] = planta_tanque(h_fuzzy[k-1], u_fuzzy[k], dt)

    # Plotagem
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    fig.suptitle('Dinâmica de Controle: Tanque com Vazamento', fontsize=14, fontweight='bold')
    cenarios = [
        (axs[0], h_onoff, u_onoff, '1. ON/OFF com Histerese (O Serrote)'),
        (axs[1], h_pid, u_pid, '2. Controlador PID (A Matemática)'),
        (axs[2], h_fuzzy, u_fuzzy, '3. Controlador Fuzzy (A Heurística)')
    ]
    for ax, h, u, titulo in cenarios:
        ax.plot(t, h, 'b-', lw=2, label='Nível (PV)')
        ax.axhline(SP, color='r', linestyle='--', label='Setpoint (SP)')
        ax.set_title(titulo, loc='left', fontweight='bold')
        ax.set_ylabel('Litros', color='b')
        ax.grid(True, linestyle=':', alpha=0.7)
        ax_u = ax.twinx()
        ax_u.fill_between(t, 0, u, color='g', alpha=0.3, step='post')
        ax_u.set_ylabel('Bomba (%)', color='g')
        ax_u.set_ylim(-5, 105)
    axs[0].legend(loc='lower right')
    plt.xlabel('Tempo (s)')
    plt.tight_layout()
    plt.show()

# =============================================================================
# 4. MENU PRINCIPAL
# =============================================================================
print("="*60)
print(" LABORATÓRIO DE CONTROLE: TANQUE COM VAZAMENTO ")
print("="*60)
print("1. Rodar Simulação Dinâmica Completa (Gráficos no Tempo)")
print("2. Modo Interativo (Depuração Matemática do Fuzzy)")
opcao = input("\nEscolha uma opção (1 ou 2): ")

if opcao == '1':
    executar_simulacao_completa()
elif opcao == '2':
    print("\n[MODO INTERATIVO INICIADO] Digite 'sair' para encerrar.")
    while True:
        entrada_n = input(f"\nDigite o Nível Atual do Tanque (Alvo = {SP}L): ")
        if entrada_n.lower() == 'sair': break
            
        entrada_v = input("Digite a Velocidade da Água (ex: -1.5 caindo, 2.0 subindo): ")
        if entrada_v.lower() == 'sair': break

        try:
            nivel = float(entrada_n)
            velocidade = float(entrada_v)

            # Cálculo do erro para o Fuzzy
            e_calc = SP - nivel
            
            # Travas de segurança do Universo de Discurso
            e_calc = max(-50, min(50, e_calc))
            velocidade = max(-10, min(10, velocidade))

            # Criação de um simulador visual limpo, sem o flush_after_run
            simulador_visual = ctrl.ControlSystemSimulation(sistema_fuzzy)

            simulador_visual.input['erro'] = e_calc
            simulador_visual.input['derro'] = velocidade
            simulador_visual.compute()
            
            pwm = simulador_visual.output['bomba']

            imprimir_matematica_fuzzy(e_calc, velocidade, pwm)

            # 1. Abre a janela visualizando o Sensor de Erro (Entrada 1)
            erro.view(sim=simulador_visual)
            plt.title(f"Fuzzificação do Erro: {e_calc:.1f}L")

            # 2. Abre a janela visualizando o Sensor de Velocidade (Entrada 2)
            derro.view(sim=simulador_visual)
            plt.title(f"Fuzzificação da Variação: {velocidade:.1f}L/s")

            # 3. Abre a janela visualizando o Motor da Bomba (Saída)
            bomba.view(sim=simulador_visual)
            plt.title(f"Centroide (Erro: {e_calc:.1f}L | Var: {velocidade:.1f}L/s) -> Bomba: {pwm:.1f}%")
            
            # Exibe todas as três janelas gráficas simultaneamente
            plt.show()

        except ValueError:
            print("[ERRO] Por favor, digite apenas valores numéricos.")
else:
    print("Opção inválida. Encerrando o programa.")
