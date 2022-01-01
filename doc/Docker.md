# Docker

### Build docker image && push
```
docker build -f docker/Dockerfile -t beentageband/ema:alpine .
docker push beentageband/ema:alpine
```
### MySQL container
create dotenv
```
cat << EOF >> .env
PGDATA=/var/lib/postgresql/data/pgdata
POSTGRES_PASSWORD=postgres
EOF
```
Create a network for psql
```
docker network create psql
docker volume create db
docker run -d --name psql --network psql --env-file .env -v db:/var/lib/postgresql/data -p 5432:5432 library/postgres:alpine
docker exec -it psql
psql -U postgres -wpostgres -p5432
```

If psql has not database, create database and user
```
docker exec -it psql sh
psql -U postgres -c "CREATE DATABASE ema;"
\q
exit
```

### SMTP container

### EMA backend container
create dotenv
```
cat << EOF >> .env
DATABASE_NAME="ema"
DATABASE_PASSWORD=postgres
DATABASE_PORT=5432
DATABASE_USERNAME=root
DJANGO_SECRET_KEY="@4&e(ylt=!_)(%s*5ewjz+apr4_5!yzlsm2cvsi6)3t!-)!qfn"
EOF
```
`$PWD` should be `path/to/ema-backend`
Attach repo to `/app` workdir to use current workspace source code.
Use `-it` to migrate database

```
docker run --network psql --env-file .env -v $PWD:/app -p 8000:8000 -it --entrypoint sh beentageband/ema:alpine 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

Finally, run django service
```
docker run -d --name ema --network psql --env-file .env -v $PWD:/app -p 8000:8000 beentageband/ema:alpine
```

#### Admin
```
hit localhost:8000/admin
```