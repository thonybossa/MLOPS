import os

# Detener todos los contenedores
os.system('sudo docker stop $(sudo docker ps -aq)')

# Eliminar todos los contenedores
os.system('sudo docker rm $(sudo docker ps -aq)')

# Eliminar todas las imágenes
os.system('sudo docker rmi $(sudo docker image ls -q)')

# Eliminar todos los volúmenes
os.system('sudo docker volume rm $(sudo docker volume ls -q)')

# Eliminar todas las redes
os.system('sudo docker network rm $(sudo docker network ls -q)')

#Eliminar img, cont, vol y redes sin utilizar
os.system('sudo docker system prune -a')

# Comprobar el estado de contenedores, imágenes, volúmenes y redes
print('#### Docker Containers ####')
os.system('sudo docker ps -a')
print()

print('#### Docker Images ####')
os.system('sudo docker image ls')
print()

print('#### Docker Volumes ####')
os.system('sudo docker volume ls')
print()

print('#### Docker Networks ####')
os.system('sudo docker network ls')
print()
