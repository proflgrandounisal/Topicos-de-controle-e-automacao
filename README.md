# Laboratório Prático: Engenharia de Sistemas Cyber-Físicos

Este repositório contém os scripts de simulação utilizados nas aulas práticas da disciplina de Sistemas Cyber-Físicos. O objetivo destes códigos é demonstrar, de forma visual e matemática, os desafios de conectar software (algoritmos) ao mundo físico (hardware e instrumentação).

## Pré-requisitos

Para executar as simulações em Python, certifique-se de ter as seguintes bibliotecas instaladas no seu ambiente:

```bash
pip install matplotlib numpy

```

---

## 1. Simulação de Malha Aberta vs. Malha Fechada (`aula1.py`)

Este script demonstra a diferença fundamental entre um sistema de controle cego (Malha Aberta) e um sistema inteligente com realimentação (Malha Fechada utilizando controle Proporcional).

### Como usar

Execute o arquivo no terminal. O script solicitará alguns parâmetros iniciais de configuração (você pode pressionar `Enter` para usar os valores padrão recomendados):

1. **Setpoint:** O nível desejado para o tanque.
2. **Ganho (Kp):** A agressividade da resposta do controlador.
3. **Vazamento Inicial:** A perturbação física base do sistema.
4. **Tempo do Incidente:** O momento (em segundos) em que uma falha física ocorrerá.
5. **Novo Vazamento:** A gravidade do incidente.

```bash
python aula1.py

```

### O que observar durante a execução

* **O Gráfico em Tempo Real:** Observe como a linha da Malha Aberta falha miseravelmente ao tentar manter o nível após o tempo do incidente (linha vertical laranja). Ela não percebe a mudança no ambiente.
* **A Correção do Erro:** A Malha Fechada identificará a queda de nível e aumentará a potência da bomba automaticamente para retornar ao Setpoint.
* **O Efeito do Ganho (Kp):** Reinicie o script e teste valores diferentes de Kp (ex: 1.0 e 15.0). Note que um Kp muito alto pode causar oscilações bruscas, enquanto um Kp muito baixo torna o sistema lento.

---

## 2. O Problema da Instrumentação (`aula2_sensores.py`)

O algoritmo de controle não enxerga o mundo real; ele enxerga o que o sensor diz a ele. Este script roda no terminal e simula a leitura de uma mesma variável de processo (nível da água subindo) através de três tipos diferentes de instrumentos.

### Como usar

Basta executar o arquivo no terminal. Ele imprimirá os dados em formato de tabela continuamente. Para interromper, pressione `Ctrl+C`.

```bash
python aula2_sensores.py

```

### O que observar durante a execução

* **A Realidade vs. Analógico:** Compare a coluna da Física com a coluna do Sensor Analógico. O analógico sofre oscilações aleatórias simulando Ruído Eletromagnético (EMI). Se um PID receber este sinal bruto, o atuador vibrará descontroladamente.
* **A Ilusão do Digital:** Observe a coluna do Sensor Digital. Devido à limitação de resolução (conversão A/D), ele fica travado no mesmo valor por vários segundos, mesmo com a água subindo, e depois "pula" bruscamente.
* **A Lógica Discreta:** A última coluna mostra um sensor de segurança (chave boia) que ignora totalmente a medição contínua e apenas avisa (0 ou 1) se um limite crítico foi atingido.

---

## 3. Simulação de Comportamento Emergente (NetLogo)

Para complementar o estudo de controle discreto, utilizaremos um modelo clássico de termostato construído em NetLogo. Ele simula a termodinâmica de um ambiente e a atuação de um sistema de Malha Fechada simples (ON/OFF).

**Acesse o simulador diretamente pelo navegador:**
[NetLogo Web: Thermostat Model](https://www.netlogoweb.org/launch#https://www.netlogoweb.org/assets/modelslib/Sample%20Models/Chemistry%20&%20Physics/Thermostat.nlogox)

### O que observar no NetLogo

1. Altere o *Target Temperature* (Setpoint).
2. Observe o comportamento da variável manipulada (o aquecedor ligando e desligando).
3. Note que, por ser um controle discreto (ON/OFF), a temperatura ambiente nunca estabiliza perfeitamente em uma linha reta; ela sempre oscila em torno do Setpoint (Histerese).

```

