# Ambiente de desenvolvimento

Neste repositório contém a solução para o desafio 3, uma API que controla uma Wallet e Cartões dos usuários.

O projeto foi desenvolvido utilizando Python 3.6.9, Django 3.0.3 e Django Rest Framework 3.11.0.

# API

A API está hospedada no Heroku na seguinte URL: https://desafio-ton-ian.herokuapp.com/

Pode ser feito o login com o superusuário já criado:

Usuário: desafio
Senha: desafio

Documentação da API: https://documenter.getpostman.com/view/8285628/SzKTweE4

# Configurações para desenvolvimento

Etapas para configurar a máquina para desenvolvimento:

- Instalar o python3 e pip3
- Instalar o virtualenv
- Criar e ativar o ambiente virtual
- Instalar as dependências do projeto, existentes no arquivo `requirements.txt`.
- Realizar as migrações do Django
- Criar um usuário admin

```bash
# Criar o ambiente virtual $python3 -m venv <nomeDoAmbienteVirtual>
$ python3 -m venv venv
# Ativar ambiente virtual $source venv/bin/activate.
$ source venv/bin/activate
# Instalar dependências
$ pip install -r requirements.txt
# Executar as migrações do Django
$ cd desafio_ton
$ python manage.py migrate
# Criar usuário admin
$ python manage.py createsuperuser
```
