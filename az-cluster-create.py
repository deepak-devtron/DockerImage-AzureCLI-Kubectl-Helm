import argparse
import json
import os
import time
import subprocess as sp


def banner(heading):
    print("-" * 35)
    print(heading)
    print("-" * 35)


parser = argparse.ArgumentParser(prog='python3 az-cluster-create.py', usage='%(prog)s [options]',
                                 description="A Script Written in Python to Create AKS cluster")

banner("Here we are storing the values of arguments that the user is passing with the command of 'python run'")

parser.add_argument("-u", "--username", required=True, help="service principal username", metavar="")
parser.add_argument("-p", "--password", required=True, help="service principal password", metavar="")
parser.add_argument("-t", "--tenant", required=True, help="service principal tenant", metavar="")
parser.add_argument("-r", "--resourceGroup", required=True, help="service principal resource group", metavar="")
parser.add_argument("-c", "--clusterName", required=True, help="service principal cluster name", metavar="")
parser.add_argument("-tag", "--tag", required=True, help="release tag for oss installation", metavar="")

args = parser.parse_args()

banner("Here we are login aws account having MFA enabled")
os.system(f"az login --service-principal -u {args.username} -p {args.password} --tenant {args.tenant}")

banner("Here we're creating ResourceGroup")
os.system(f"az group create --name {args.resourceGroup} --location eastus")
time.sleep(5)

banner("Here we are creating AKS cluster")
os.system(
    f"az aks create --resource-group {args.resourceGroup} --node-vm-size B4ms --name {args.clusterName} --node-count 1 --generate-ssh-keys --enable-node-public-ip")
print("cluster creation complete..")

banner("Here we are getting aks credentials")
os.system(f"az aks get-credentials --resource-group {args.resourceGroup}  --name {args.clusterName}")

banner("Here we are installing Devtron in our freshly created cluster")
sp.getoutput("wget https://raw.githubusercontent.com/prakarsh-dt/kops-cluster/main/devCluster/devtron-ucid.yaml")
os.system("kubectl create namespace devtroncd")
os.system("kubectl apply -f devtron-ucid.yaml -ndevtroncd")
banner("devtron-ucid has been applied in devtroncd ns")
os.system("rm devtron-ucid.yaml")
os.system("helm repo add devtron https://helm.devtron.ai/")
os.system("helm install devtron devtron/devtron-operator --namespace devtroncd --set installer.modules={cicd} --set " +f"installer.release={args.tag}")

banner("Here we are checking installation status of application")
os.system("sleep 2")
os.system("touch status.txt")

while sp.getoutput("cat status.txt") != "Applied":
    sp.getoutput(
        "kubectl -n devtroncd get installers installer-devtron -o jsonpath='{.status.sync.status}' > status.txt")
    os.system("sleep 90")
    if sp.getoutput("cat status.txt") == "Downloaded":
        print("\nStill Downloading Microservices : ", end="")
        os.system("cat status.txt")
        print("\n")
        os.system("kubectl get pods -ndevtroncd")
    else:
        continue
print("devtron installation complete..")
banner("Here we are getting dashboard url")
BaseServerUrl = sp.getoutput(
    "kubectl get svc -n devtroncd devtron-service  -o jsonpath='{.status.loadBalancer.ingress[0].ip}'")

banner("Here we are getting admin password")
LoginPassword = sp.getoutput(
    "kubectl -n devtroncd get secret devtron-secret -o jsonpath='{.data.ACD_PASSWORD}' | base64 -d")

Credentials = {"LOGIN_USERNAME": "admin", "BASE_SERVER_URL": "http://"+BaseServerUrl,
               "LOGIN_PASSWORD": LoginPassword}

banner("Here we are setting credentials in a json file mounted over working container")
credentialsJson = json.dumps(Credentials, indent=4)
f = open("/base-test/credentials.json", 'w')
f.write(credentialsJson)
f.close()
