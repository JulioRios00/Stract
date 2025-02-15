# Stract - Processo Seletivo

Repositório criado exclusivamente para teste técnico para vaga de desenvolvedor de software na Stract.

##

1 - Crie um ambiente virtual e instale as dependências do projeto.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2- Execute o servidor local com o comando:
```bash
python app/main.py
```

3- Acesse o servidor local em seu navegador através do endereço. :
```bash
http://localhost:5000
```

## Endpoints

_Plataformas_
```
GET /<platform> - Traz todos os ads de uma plataforma especifica
```

```
GET /<platform>/resumo - Traz um resumo de todos os ads de uma plataforma
```
```
GET /<platform>/download - Download dos ads de uma plataforma por CSV
```

_Geral_

```
GET /geral - Traz todos os dados gerais
```
```
GET /geral/resumo - Traz um resumo de todas as plataformas
```
```
GET /geral/download - Download do resumo de todas as plataformas por CSV
```
