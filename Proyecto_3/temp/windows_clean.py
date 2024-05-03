import os

# Detener todos los contenedores
os.system('powershell "docker stop $(docker ps -aq)"')

# Eliminar todos los contenedores
os.system('powershell "docker rm $(docker ps -aq)"')

# Eliminar todas las imágenes
os.system('powershell "docker rmi $(docker image ls -q)"')

# Eliminar todos los volúmenes
os.system('powershell "docker volume rm $(docker volume ls -q)"')

# Eliminar todas las redes
os.system('powershell "docker network rm $(docker network ls -q)"')

# Comprobar el estado de contenedores, imágenes, volúmenes y redes
print('#### Docker ####')
os.system('powershell "docker ps -a"')
print()
print('#### Docker Images ####')
os.system('powershell "docker image ls"')
print()
print('#### Docker Volumes ####')
os.system('powershell "docker volume ls"')
print()
print('#### Docker Networks ####')
os.system('powershell "docker network ls"')