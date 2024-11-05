# create database name 'db_fastapi'
# create '.env' file


*********** add the following lines into .env ************
SECRET_KEY=
ALGORITHM=HS256
ENV=local
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/db_fastapi
URL_ONE=http://localhost:3000
URL_TWO=https://localhost:3000


******** run command for SECRET_KEY *********
*** openssl rand -hex 32
# paste the key to SECRET_KEY

SECRET_KEY=
ALGORITHM=HS256
ENV=local
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/db_fastapi
URL_ONE=http://localhost:3000
URL_TWO=https://localhost:3000


******** then run this commands *********
# python3 -m venv env
# source env/bin/activate
# pip3 install -r requirements.txt
# cd src
# alembic upgrade head
# python3 main.py 