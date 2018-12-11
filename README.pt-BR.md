Wiim Industrial Information Management
======
*Read this in other languages: [English](README.md), [Português (BR)](README.pt-BR.md).*

Trabalho de Conclusão de Curso
------
Aplicativo de servidor do Wiim.

Requerido
------
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

Uso
------
Para instalar ou atualizar o banco de dados:
```
python manage.py db upgrade
```
Para iniciar o servidor:
```
python manage.py run
```

Licença
------
`CC BY-NC 4.0` – [Atribuição-NãoComercial 4.0 Internacional](https://creativecommons.org/licenses/by-nc/4.0/deed.pt_BR)