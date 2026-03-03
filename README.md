# Tópicos de Controle e Automação: Simulações em Python

Repositório oficial de apoio à disciplina de Tópicos de Controle e Automação (Engenharia da Computação), focado no desenvolvimento do projeto prático **SmartFlow**.

**Docente:** Prof. Dr. Leonardo Grando  
**Período:** 1º Semestre / 2026  

## Sobre o Repositório

Este repositório contém os scripts desenvolvidos em sala de aula para demonstrar a aplicação da teoria de controle em sistemas cibernéticos. O objetivo é fornecer uma base em código (Python) para que os Squads possam modelar, simular e validar a arquitetura de seus projetos (TCC e SmartFlow) antes da implementação em hardware físico.

## Contexto: Metodologia PBL

O desenvolvimento segue a divisão do projeto em Sprints. Os códigos atuais dão suporte à **Sprint 1: Modelagem e Arquitetura**, permitindo a abstração de sistemas físicos ou arquiteturas de software (Plantas) em modelos matemáticos discretos (Gêmeos Digitais).

## Estrutura de Arquivos

A evolução dos scripts acompanha a ementa da disciplina:

* **`aula1.py`**: Simulação introdutória comparando o comportamento de um sistema operando em Malha Aberta versus Malha Fechada perante uma perturbação externa.
* **`aula2_sensores.py`**: Experimento prático sobre Instrumentação Industrial. Demonstra o impacto do ruído analógico, da perda de resolução (quantização digital) e do atraso de sensores discretos na leitura da Variável de Processo (PV).
* **`aula3_modelagem.py`**: Implementação da arquitetura de um Diagrama de Blocos utilizando Programação Orientada a Objetos (OOP).

## Foco Teórico: Modelagem em Tempo Discreto (`aula3_modelagem.py`)

O script da Aula 3 é o alicerce metodológico para as simulações dos Squads. Ele divide o sistema de controle em quatro classes independentes, refletindo com exatidão matemática o fluxo de sinal de um Diagrama de Blocos:

1. **`Planta`**: Representa o fenômeno dinâmico controlado. Utiliza uma Equação de Diferenças para calcular o estado futuro com base na inércia do sistema e no tempo de amostragem ($\Delta t$).
   $$h_{k+1} = h_k + \frac{(Q_{in} - Q_{out}) \cdot \Delta t}{A}$$
2. **`Sensor`**: Abstrai a leitura da grandeza física (PV), atuando como a fronteira de conversão de dados.
3. **`Atuador`**: Converte o esforço computacional (Sinal de Controle, $u(t)$) em ação de engenharia, respeitando os limites operacionais físicos (saturação).
4. **`Controlador`**: O núcleo algorítmico que calcula o Erro em tempo real ($E = SP - PV$) e define a ação corretiva matemática.

## Requisitos e Execução

Para executar as simulações, é necessário um ambiente Python 3 configurado com as bibliotecas de processamento numérico e plotagem gráfica.

**Dependências:**
```bash
pip install numpy matplotlib

```

**Execução:**

```bash
python aula3_modelagem.py

```

## Próximos Passos (Sprint 2)

A aprovação da arquitetura desenvolvida nesta etapa é pré-requisito para o avanço do projeto. Os modelos validados servirão de ambiente de testes para a Sprint 2, onde implementaremos as lógicas de Controle Avançado, iniciando pelos algoritmos Liga/Desliga com Histerese e avançando para a estrutura completa do PID.

```

Com o repositório devidamente documentado e o material da aula 05/03 finalizado, gostaria que eu iniciasse o rascunho dos conceitos teóricos (Liga/Desliga e Histerese) para a aula da semana que vem (12/03)?

```
