# API de resultados da Loteria
Desenvolvimento de uma API para resultados da loteria (Megasena e LotoFácil) utilizando um webcrawler com raspagem de dados para obter os dados diretamente do site da Caixa Econômica


# Instalação

### Instale os pacotes necessários
```
1) $ python3.6 -m venv ./env
2) $ source env/bin/activate
3) $ pip install -r config/requirements.txt
```
### Defina as variáveis de ambiente e rode o projeto
```
4) $ export FLASK_ENV=development
5) $ export FLASK_APP=main
6) $ cd src && flask run
```


# Libraries

- Selenium
- Flask
- Typing
- Regex
- BeautifulSoup