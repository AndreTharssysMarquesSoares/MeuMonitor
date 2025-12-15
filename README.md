# 📘 Guia de Configuração e Fluxo de Trabalho

Este guia contém o passo a passo para configurar o ambiente de desenvolvimento e o padrão de trabalho da equipe.

---

## 🚀 Parte 1: Configuração Inicial (Apenas uma vez)

Siga estes passos ao entrar no projeto pela primeira vez.

### 1. Clonar o Repositório
Abra o terminal na pasta onde você guarda seus projetos e rode:

```bash
git clone SEU_LINK_DO_GITHUB_AQUI
cd meumonitor
```

### 2. Criar o Ambiente Virtual (Venv)
O ambiente virtual não vem pelo Git. Cada desenvolvedor cria o seu localmente:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
Instale as bibliotecas com as versões exatas definidas no projeto:

```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados Local
Crie o banco de dados localmente (o banco não é versionado por segurança):

```bash
python manage.py migrate
```

### 5. Testar a Instalação
Rode o servidor para garantir que tudo está certo:
```bash
python manage.py runserver
```