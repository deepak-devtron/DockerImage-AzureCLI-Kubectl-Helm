import os
import argparse

parser = argparse.ArgumentParser(prog='python3 cluster-create.py', usage='%(prog)s [options]',
                                description="A Script Written in Python to Create Single Node Kops Cluster")

#Here we are storing the values of arguments the user is passing with the command of "python run"
parser.add_argument("-c", "--username", required=True, help="service principal username", metavar="")
parser.add_argument("-r", "--password", required=True, help="service principal password", metavar="")
parser.add_argument("-b", "--tenant", required=True, help="service principal tenant", metavar="")
parser.add_argument("-b", "--resourceGroup", required=True, help="service principal tenant", metavar="")
parser.add_argument("-b", "--clusterName", required=True, help="service principal tenant", metavar="")

args = parser.parse_args()

#Here we login aws account having MFA enabled
os.system("az login --service-principal -u args.username -p args.password --tenant args.tenant")

#Here we creating ResourceGroup
os.system("az group create --name args.resourceGroup --location eastus")

#Here we are creating AKS cluster
os.system("az aks create --resource-group args.resourceGroup --name args.clusterName --node-count 1 --generate-ssh-keys --enable-node-public-ip")

# Here we are getting aks credentials
os.system("az aks get-credentials --resource-group args.resourceGroup  --name args.clusterName")

#Here we are creating repo for devtron installation
os.system("helm repo add devtron https://helm.devtron.ai/")

#Here we are installing Devtron on our freshly created cluster
os.system("helm install devtron devtron/devtron-operator --create-namespace --namespace devtroncd")


#os.system("az aks delete --resource-group {nameForResourceGroup} --name {nameForCluster}")