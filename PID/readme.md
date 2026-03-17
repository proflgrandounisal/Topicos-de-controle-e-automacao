# Laboratório PID

Este repositório contém o script de simulação `laboratorio_pid.py`, projetado para demonstrar visual e matematicamente a evolução dos sistemas de controle em malha fechada. O objetivo é afastar o aluno da simples "cópia de fórmulas" e introduzi-lo à análise de **causalidade dinâmica em tempo real**.

O código simula um sistema térmico de primeira ordem (Planta Física) e aplica diferentes lógicas de controle (do rudimentar Liga/Desliga ao algoritmo PID completo). A simulação expõe os problemas físicos reais que os engenheiros de computação enfrentam ao integrar software e hardware, como saturação de atuadores, ruído de leitura e o fenômeno de *Chattering*.

## Pré-requisitos

O simulador foi desenvolvido em Python. Para executá-lo, certifique-se de ter as seguintes bibliotecas instaladas no seu ambiente virtual:

```bash
pip install numpy matplotlib
```

## Como Executar

Clone o repositório e execute o script diretamente via terminal. O código gerará um *dashboard* com seis gráficos comparativos.

```bash
python laboratorio_pid.py
```

## Cenários Simulados (Guia de Análise Socrática)

Ao executar o simulador, o aluno deve analisar criticamente os 6 gráficos gerados (Eixo Y Esquerdo: Temperatura e Erro; Eixo Y Direito: Esforço do Atuador).

1. **ON/OFF (O Chattering e a Destruição do Atuador):** Demonstra como o ruído microscópico do sensor força o atuador a ligar e desligar freneticamente ao redor do Setpoint, o que causaria a queima prematura de componentes eletromecânicos no chão de fábrica.
2. **Histerese (Proteção de Hardware):** Mostra a implementação de uma "Banda Morta". A histerese reduz a frequência de chaveamento do motor (salvando o hardware), mas ao custo de manter a Variável de Processo (PV) em constante oscilação.
3. **Somente [P] (Ação Proporcional):** Apresenta o controlador analógico básico. O aluno observará o "Erro de Regime Permanente" (Offset), provando que o ganho proporcional perde força à medida que se aproxima do Setpoint e empata com a inércia térmica da planta.
4. **[P] + [I] (Ação Integral):** Demonstra como a memória matemática (acúmulo do erro no tempo) elimina o erro de regime. No entanto, o aluno deve notar o surgimento do *Overshoot* (a temperatura ultrapassa o alvo antes de estabilizar).
5. **[P] + [I] + [D] (Ação Derivativa e Sintonia Ideal):** Apresenta o sistema perfeitamente sintonizado. A derivada atua como um freio preditivo, zerando o Overshoot e garantindo um tempo de acomodação rápido e suave.
6. **O Perigo do [D] (Caos Derivativo):** Injeta-se um ruído de alta frequência na leitura do sensor. A derivada amplifica essa interferência, resultando em surtos de potência destrutivos no motor. Este cenário introduz a necessidade de Filtros Digitais (Sprint 3).

## Estrutura do Código e Arquitetura

O script está modularizado para refletir o Diagrama de Blocos padrão de um sistema cibernético:

* `planta_aquecedor(T_atual, U_atual, ruido, dt)`: Representa o Gêmeo Digital. Simula a equação de diferenças do mundo físico contendo inércia térmica e perturbações.
* `simular_controle(...)`: Representa o microcontrolador. Contém o laço de amostragem no tempo discreto (`dt`), o cálculo do Erro Relativo, as lógicas de controle (ON/OFF, Histerese, PID) e a proteção de *Anti-Windup* para lidar com a saturação física do atuador (0% a 100%).

## Missão dos Squads (Sprint 2)

Os alunos devem utilizar este repositório como base para:
1. Extrair a lógica discreta do PID e integrá-la às classes de controle do projeto TCC.
2. Implementar a proteção de Anti-Windup nos motores/bombas reais.
3. Realizar a sintonia empírica ($Kp$, $Ki$, $Kd$) da própria malha para minimizar o Overshoot e o Tempo de Acomodação.
