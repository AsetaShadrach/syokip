<!--  -->
# Minimalistic implementation of IP allocator


### To run
First run <br>
`docker-compose up -d db` <br>
Then <br>
`docker ps` <br>
Then copy the container ID for the db(mysql) and run <br>
`docker exec -it {CONTAINER_ID} bash` <br>
When inside the container run <br>
`mysql -u {MYSQL_USER} -p{MYSQL_PASSWORD}` <br>
Then run <br>
`CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};` <br>
Then exit the container <br>

## Improvements:
- Auth
- .sh Entrypoint
- autocreate db if missing
- move all env type variables to env
- Add unllocated ips to get
- Still working on (production) addons for redis and Postgres


## Endpoints
- {{base_url}}/allocate
- {{base_url}}/release/{ip}
- {{base_url}}/allocated
- {{base_url}}/available