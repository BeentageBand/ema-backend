# Docker

### MySQL container

```
cat << EOF >> .env
MYSQL_ROOT_PASSWORD=password
EOF
```

```
sudo docker volume create db
sudo docker run -d --env-file .env -v db:/var/lib/postgresql/data -p 5432:5432 library/postgres:alpine
```

### SMTP container

### EMA backend container

```
cat << EOF >> .env
DATABASE_NAME="ema"
DATABASE_PASSWORD="password"
DATABASE_PORT="32027"
DATABASE_USERNAME="root"
DJANGO_SECRET_KEY="@4&e(ylt=!_)(%s*5ewjz+apr4_5!yzlsm2cvsi6)3t!-)!qfn"
EOF
```

```
sudo docker run -d --env-file .env -v $PWD:/app -p 8000:8000 --entrypoint bash beentageband/ema:alpine entrypoint.sh
sudo docker run -d --env-file .env -v $PWD:/app -p 8000:8000 beentageband/ema:alpine
```

