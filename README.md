# Portal de Integração Helpdesk GLPI

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![React Version](https://img.shields.io/badge/react-18%2B-61dafb.svg)](https://reactjs.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

Este projeto é uma solução moderna de interface para o sistema de chamados GLPI. Desenvolvido com uma arquitetura desacoplada, o portal visa simplificar a experiência do usuário final na abertura e acompanhamento de tickets, integrando-se via API ao motor do GLPI.

## 🚀 Visão Geral

O sistema atua como uma camada intermediária (middleware) que consome a API do GLPI e entrega uma interface performática e intuitiva. Ideal para empresas que buscam customizar a jornada do usuário sem perder a robustez do backend do GLPI.

### 🛠️ Tecnologias Utilizadas

**Backend:**
*   **Linguagem:** [Python 3.10+](https://www.python.org/)
*   **Gerenciamento de Ambiente:** `venv` (Virtual Environment)
*   **Integração:** GLPI API Wrapper

**Frontend:**
*   **Framework:** [React.js](https://reactjs.org/)
*   **Gerenciamento de Pacotes:** `npm` / `node.js`

---

## 🏗️ Estrutura do Projeto

```text
helpdesk-glpi/
├── backend/            # Lógica do servidor e integração com API GLPI
│   ├── venv/           # Ambiente virtual (não versionado)
│   └── main.py         # Ponto de entrada da aplicação Python
├── src/                # Código-fonte do Frontend (React)
├── .gitignore          # Regras de exclusão do Git
└── README.md           # Documentação principal