

==============================================================================
Projetos_Manutenção Veicular
==============================================================================

   
Tecnologias Utilizadas
======================

* **Python** (gerenciado com pyenv)
* **Docker**
* **Docker Compose**
* **Django** ------------------------------------------------------------------------------------------
***Flask**

Pré-requisitos
==============

Certifique-se de que as seguintes ferramentas estão instaladas e configuradas na sua máquina.

1.  Python (com pyenv)
---------------------

A forma recomendada para instalar e gerenciar versões do Python é com o **pyenv**. Ele permite que você alterne facilmente entre versões sem conflitos.

**macOS (via Homebrew)**

.. code-block:: bash .

    $ brew install pyenv

**Linux (via curl)**

.. code-block:: bash

    $ curl https://pyenv.run | bash

*Após a instalação, siga as instruções no terminal para adicionar o pyenv ao seu PATH.*

*O Flask irá iniciar um servidor web

*
2.  Git
-------

O **Git** é essencial para clonar o repositório.

**Windows**

* Baixe o instalador oficial em: `https://git-scm.com/download/win`

**macOS (via Homebrew)**

.. code-block:: bash

    $ brew install git

**Linux (via gerenciador de pacotes)**

*Para sistemas baseados em Debian/Ubuntu, use:*

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get install git
------------------------------------------------------------------------------------------

Configuração e Execução
=======================

Siga os passos abaixo para colocar o projeto em funcionamento.

1. **Clonar o Repositório**


Primeiro, clone o projeto para sua máquina local usando o Git.

.. code-block:: bash

    $ git clone https://github.com/seu-usuario/seu-repositorio.git
    $ cd seu-repositorio
     

2.  **Configuração do Ambiente Python**
    
    Use `pyenv` para instalar a versão do Python desejada:
    
    .. code-block:: bash
    
        $ pyenv install 3.13.7
        $ pyenv local 3.13.7
        # Instale as dependências a partir do arquivo requirements.txt
        # pip install
        $ pip install -r requirements.txt
        $ pip freeze > requirements.txt

    
------------------------------------------------------------------------------------------

Acesso à Aplicação
==================
* Abra seu terminal na mesma pasta onde você salvou o arquivo  app.py.
Crie o ambiente virtual
*  python3 -m venv venv
Ative o ambiente virtual
*  source venv/bin/activate

Execute o servidor com o comando:
* python app.py

**O Flask irá iniciar um servidor web

Após a execução bem-sucedida, a aplicação estará disponível noendereço:

* Página Principal (Lista de Tarefas): *

    Acesse no seu navegador:  http://127.0.0.1:5000/ 

* **Painel de Administração:**
    

