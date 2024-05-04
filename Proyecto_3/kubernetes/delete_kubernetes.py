import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"Command: {command}\nOutput: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing {command}: {e.stderr}")

def main():
    #Eliminar kubernetes
    run_command("sudo microk8s kubectl delete --all daemonsets,replicasets,services,deployments,pods,rc,ingress --namespace=default")

if __name__ == "__main__":
    main()
