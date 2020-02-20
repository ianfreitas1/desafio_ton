# API

A API está hospedada no Heroku na seguinte URL: https://desafio-ton-ian.herokuapp.com/

Pode ser feito o login com o superusuário já criado:

Usuário: desafio
Senha: desafio

Documentação da API: todo

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
