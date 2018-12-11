Wiim Industrial Information Management
======
*Read this in other languages: [English](README.md), [Português (BR)](README.pt-BR.md).*

Undergraduate Final Project
------
Desktop server application.

Requires
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

Usage
------
To install or upgrade database:
```
python manage.py db upgrade
```
To run server:
```
python manage.py run
```

License
------
`CC BY-NC 4.0` – [Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/)