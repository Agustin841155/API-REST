# API-REST
CREACION DE API REST Y SU USO
## creacion de imagen 
docker build -t imagen_api:v1 .

## creacion de contenedor basado en imagen

docker run -it - v "PWD"/home:/home/code --net=host --name api_rest -h agustin imagen_api:v1
