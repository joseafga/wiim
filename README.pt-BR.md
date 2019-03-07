# Wiim Industrial Information Management
*Read this in other languages: [English](README.md), [Português (BR)](README.pt-BR.md).*

### Trabalho de Conclusão de Curso
Aplicativo de servidor do Wiim.

## Requerido
* pip install pyqt5
* pip install opcua (*cryptography, dateutil, lxml and pytz)
* pip install opcua-widgets
* pip install cryptography
* pip install flask
* pip install flask-sqlalchemy flask-caching flask-migrate flask-script
* pip install flask-marshmallow marshmallow-sqlalchemy
* pip install pymysql
* pip install qrcode
* pip install Pillow

## Uso
Para instalar ou atualizar o banco de dados:

    python manage.py db upgrade

Para iniciar o servidor:

    python manage.py run


### Licença
Livre para uso pessoal, para uso comercial, por favor, contate-nos.  
`Licença AGPLv3/Comercial` - veja o arquivo [LICENSE](LICENSE "Arquivo de licença") para mais detalhes.
