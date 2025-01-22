# INSABA Rest Api BoilerPlate
Merupakan starter kit untuk membuat rest api dengan konsep microservice yang terhubung dengan InSaba SSO (Single Signed On). Project ini tidak memiliki mekanisme login ataupun role, semua fungsi tersebut telah diatur oleh sso.

# Features
* Database ORM with [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* Database Migrations using [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)
* JSON Web Token Authentication with [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
* Swagger Documentation (Part of Flask-RESTX).
* Full featured framework for fast, easy, and documented API with [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
* Object serialization/deserialization with [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
* Data validations with Marshmallow [Marshmallow](https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation)
* -----------------------------------------------------------##
* Telah disediakan decorator **@token_required** yang dapat digunakan pada setiap resource / endpoint kamu, lalu jika decorator tersebut berhasil, maka kamu bisa memanggil variable **current_user** yang sudah berisi data user claim dari sso. 
* Add example for Dynamic Documentation and SqlAlchemy Query service.
* SqlAlchemy example : Telah ditambahkan event trigger di setiap model/tabel ```do_orm_execute, before_insert, before_update, before_delete``` untuk membatasi akses terhadap id_unit sebelum melakukan eksekusi pada database.
* SqlAlchemy example : Telah ditambahkan event trigger di setiap model/tabel ```after_insert, after_update, after_delete``` untuk mencatat aktifitas user ke sso.


# Pre-requisites
It uses [Black](https://github.com/psf/black) for code styling/formatting.

# Python Project Installation
1. Make sure python 3.9^ is installed on your operating system.
2. Open this project folder and set the python interpreter with your global python, then activate virtual env for this project.
4. Go to terminal and install all dependency package with command ```pip install -r requirements.txt```

# Setup Project
1. Open file **.env** then edit value of **DOMAIN** with your domain app name & edit value of **DATABASE** with your connection string to database
2. Example of Basic CRUD is in the folder app/api/sample. Create a new with copy and paste to your folder app/api/{YOUR_MODEL}.
3. Open on app/api/{YOUR_MODEL}/_init_.py and set all variables 
follow the example and focus on model.py for migration database schema with sqlalchemy.
5. When it's all done, open a terminal and type command ```flask clear_and_seed``` 
to generate a database, all schemas, and all tables, according to the database connection you set in .env and according to the sqlalchemy model you created. This Method Using **DROP AND CREATE**. Be Careful!
6. Right click on file run.py in root folder, then click run.
7. App is Running on http://127.0.0.1:5000/ by default.

## CLI command output:
```sh
Commands:
  flask clear_and_seed  #to generate a database, all schemas, and all tables.
```

## Notes
- By default the `/` route is used by the `all` blueprint.
- **Database Fields Pattern** : in your database, for the **id** field name must use the name **"`id`"** (lowercase) in each table.
- If there is a field that has a **unit** identity like ; unitkey, idUnit, unitId, unit_id, and others, then the field name must be **"`id_unit`"** (lowercase) in each table.
- `virtualenv` is recommended to manage your packages and Python environment, hence why `requirements.txt` has been generated.