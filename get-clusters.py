import json
from azure.cli.core import get_default_cli
import subprocess

subscription  = {"PRD - Online" : "90e3f5d9-3731-4c45-a3f1-419fbc97f996", "PRD - Online 2" : "9f66adb7-6721-4ca4-953e-e2b4b864803c","PRD - Inteligencia Operacional" : "5a228de8-f1ab-4c19-9d20-6ed918f6e81f", "PRD - DataScience" : "e4128695-83c0-493e-89db-2095acf2d7c6", "PRD - Lojas" : "7caa6be6-25dc-44ae-bf8f-cd2a01fea109", "PRD - Backoffice" : "819a7d8f-1b0a-4121-b7dc-d001d9f109f1"}


if __name__ == '__main__':

    for subname, subid in subscription.items():
        get_default_cli().invoke(['account', 'set', '--subscription', subid])
        akslist = subprocess.Popen(['az', 'aks', 'list'], stdout=subprocess.PIPE)
        out, err = akslist.communicate()
        aks_list_json = json.loads(out)
        for cluster in aks_list_json:
            print(f'Resource Group: {cluster["resourceGroup"]} --> Cluster Name: {cluster["name"]}')
            get_default_cli().invoke(['aks', 'get-credentials', '--resource-group', cluster["resourceGroup"], '--name', cluster["name"], '--admin'])

            
