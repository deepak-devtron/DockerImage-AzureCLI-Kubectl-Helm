import argparse
import os
import time

parser = argparse.ArgumentParser(prog='python3 az-cluster-create.py', usage='%(prog)s [options]',
                                 description="A Script Written in Python to Create AKS cluster")

# Here we are storing the values of arguments the user is passing with the command of "python run"
parser.add_argument("-u", "--username", required=True, help="service principal username", metavar="")
parser.add_argument("-p", "--password", required=True, help="service principal password", metavar="")
parser.add_argument("-t", "--tenant", required=True, help="service principal tenant", metavar="")
parser.add_argument("-r", "--resourceGroup", required=True, help="service principal tenant", metavar="")
parser.add_argument("-c", "--clusterName", required=True, help="service principal tenant", metavar="")

args = parser.parse_args()

# Here we are login aws account having MFA enabled
os.system(f"az login --service-principal -u {args.username} -p {args.password} --tenant {args.tenant}")

# Here we're creating ResourceGroup
os.system(f"az group create --name {args.resourceGroup} --location eastus")
time.sleep(10)

# Here we are creating AKS cluster
os.system(
    f"az aks create --resource-group {args.resourceGroup} --name {args.clusterName} --node-count 1 --generate-ssh-keys --enable-node-public-ip")
time.sleep(600)
# Here we are getting aks credentials
os.system(f"az aks get-credentials --resource-group {args.resourceGroup}  --name {args.clusterName}")

# Here we are creating repo for Devtron installation
os.system("helm repo add devtron https://helm.devtron.ai/")

# Here we are installing Devtron on our freshly created cluster
os.system("helm install devtron devtron/devtron-operator --create-namespace --namespace devtroncd")
time.sleep(1200)

# Here we are getting all the pods in devtroncd namespace
os.system("kubectl get po -ndevtroncd")

# Here we are deleting azure resource group
os.system(f"az group delete -y --name {args.resourceGroup}")
