import time
import random

def iniciar_comparativo_completo():
    print("--- INICIANDO VARREDURA DOS 3 TIPOS DE SENSORES ---")
    print("Processo: Enchimento do Tanque a partir de 50 Litros")
    print("Alarme de Nivel Alto (Sensor Discreto) configurado para 65 Litros\n")
    
    # Cabecalho do terminal
    print(f"{'TEMPO':<6} | {'REALIDADE':<15} | {'ANALOGICO (RUIDO)':<25} | {'DIGITAL (RESOLUCAO)':<25} | {'DISCRETO (ALARME)'}")
    print("-" * 95)

    nivel_real_base = 50.0
    segundos = 0

    try:
        while True:
            # 1. A realidade fisica (subindo 0.4 L por segundo)
            nivel_variando = nivel_real_base + (segundos * 0.4)

            # 2. Sensor Analogico (Adicionando ruido de -3.5 a +3.5)
            interferencia = random.uniform(-3.5, 3.5)
            leitura_analogica = nivel_variando + interferencia
            
            # 3. Sensor Digital (Degraus de 10 em 10 Litros)
            leitura_digital = round(nivel_variando / 10.0) * 10.0
            
            # 4. Sensor Discreto (Chave boia simples: 0 ou 1)
            # Ele e cego para o nivel, so avisa se bater no limite fisico de 65L
            if nivel_variando >= 65.0:
                leitura_discreta = "1 (LIGADO - ALERTA)"
            else:
                leitura_discreta = "0 (DESLIGADO)"

            # Formatacao para impressao limpa no terminal
            c_tempo = f"{segundos}s"
            c_real = f"{nivel_variando:.1f} L"
            c_ana = f"{leitura_analogica:.1f} L"
            c_dig = f"{leitura_digital:.1f} L"
            
            print(f"{c_tempo:<6} | {c_real:<15} | {c_ana:<25} | {c_dig:<25} | {leitura_discreta}")
            
            segundos += 1
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nVarredura interrompida.")

if __name__ == "__main__":
    iniciar_comparativo_completo()
