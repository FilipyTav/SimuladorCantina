# Simulador de Cantina

O **Simulador de Cantina** é um sistema de gerenciamento de pedidos e estoque. O projeto foca na aplicação prática de estruturas de dados lineares e encadeadas.

---

##  Arquitetura de Dados

Foram usadas dIferentes estruturas de dados para cada funcionalidade:

* **Produtos (Fila de Prioridade):** Gerenciados através de uma **Lista Duplamente Encadeada**. Isso permite a inserção e remoção eficiente de itens com base em níveis de prioridade, nesse caso, data de validade, permitindo navegação para frente e para trás na fila.

* **Pagamentos (Histórico):** Implementados como uma **Lista Simplesmente Encadeada** para o registro sequencial de transações onde o foco é o percurso unidirecional dos dados.

* **Navegação (Interface):** Os menus do sistema são controlados por uma **Pilha (Stack)**, seguindo a lógica LIFO (*Last-In, First-Out*). Isso permite que o usuário "entre" em submenus e retorne ao menu anterior.

---

## Estrutura do Projeto

| Diretório / Arquivo | Descrição |
| :--- | :--- |
| `src/main.py` | Ponto de entrada da aplicação. |
| `src/ui.py` | Gerencia a interface de usuário e a lógica de exibição de menus. |
| **src/structs/** | **Núcleo de Estruturas de Dados** |
| ├─ `pqueue.py` | Implementação da Fila de Prioridade com as classes `PNode` e `PQueue`. |
| ├─ `product.py` | Define a classe `Product`. |
| ├─ `menu.py` | Estrutura base para o manuseamento de menus do sistema. |
| ├─ `menu_stack.py` | Pilha para controle de navegação entre menus. |
| ├─ `payment.py` | Define a classe `Payment` e a lógica de processamento de pagamentos. |
| └─ `payment_history.py` | Implementação da Lista Encadeada com as classes `PaymentNode` e `PaymentLedger`. |
| **src/utils/** | **Auxiliares e Configurações** |
| ├─ `gen_dummy_data.py` | Script para popular o sistema com dados fictícios para teste. |
| ├─ `input.py` | Tratamento e validação de entradas do usuário no terminal. |
| ├─ `save_data.py` | Lógica de persistência de dados em arquivos locais. |
| └─ `types.py` | Definições de tipos customizados e enums para o sistema. |

---

## Como Executar

### 1. Pré-requisitos
* **Python 3.10** ou superior.

### 2. Instalação
1. Clone o repositório para sua máquina:
```bash
git clone https://github.com/FilipyTav/SimuladorCantina.git
cd SimuladorCantina
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/Scripts/activate
```
3. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

### 3. Execução
Execute o arquivo principal:
```bash
python src/main.py
```