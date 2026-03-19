# 🧠 MiniCPU – Simulador Fetch-Decode-Execute (Bubble Sort)

## 👥 Integrantes

- Bernardo Heuer, bchg@cesar.school  
- Eduardo Roma, erca@cesar.school  

## 📌 Descrição do Projeto

Este projeto consiste na implementação de um simulador de CPU simples (MiniCPU), desenvolvido em Python, com o objetivo de reproduzir o funcionamento básico de um processador real através do ciclo:

FETCH > DECODE > EXECUTE

O simulador executa instruções armazenadas em memória, manipulando registradores e realizando operações conforme um conjunto de instruções (ISA) pré-definido.

## 📌 Linguagem Utilizada

Python

## ⚙️ Arquitetura da MiniCPU

A CPU simulada possui:

- **Registradores:**
  - R0, R1, R2, R3 (8 bits, valores de 0 a 255)

- **Outros componentes:**
  - PC (Program Counter)
  - ZF (Zero Flag)

- **Memória:**
  - 256 posições (0x00 a 0xFF)

