import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"Command: {command}\nOutput: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing {command}: {e.stderr}")

def main():
    # Descargar kompose
    run_command("curl -L https://github.com/kubernetes/kompose/releases/download/v1.26.0/kompose-linux-amd64 -o kompose")

    # Hacer kompose ejecutable
    run_command("chmod +x kompose")

    # Mover kompose al directorio de binarios
    run_command("sudo mv ./kompose /usr/local/bin/kompose")

    # Convertir docker-compose.yml
    run_command("kompose convert -f docker-compose.yml -o komposefiles/ --volumes hostPath")

    # Aplicar configuraciones con kubectl
    run_command("sudo microk8s kubectl apply -f komposefiles/")

    # Mostrar todos los recursos de kubernetes
    run_command("sudo microk8s kubectl get all --all-namespaces")

    # Obtener información de los servicios
    run_command("sudo microk8s kubectl get service")

    # Obtener información de los servicios nuevamente
    run_command("sudo microk8s kubectl get pods")

if __name__ == "__main__":
    main()
