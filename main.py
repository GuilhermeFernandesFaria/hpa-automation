from kubernetes import client, config
import kubernetes.client
from azure.cli.core import get_default_cli
import subprocess
import json

configuration = kubernetes.client.Configuration()
subscription = {"PRD - Online": "90e3f5d9-3731-4c45-a3f1-419fbc97f996", "PRD - Online 2": "9f66adb7-6721-4ca4-953e-e2b4b864803c", "PRD - Inteligencia Operacional": "5a228de8-f1ab-4c19-9d20-6ed918f6e81f", "PRD - DataScience": "e4128695-83c0-493e-89db-2095acf2d7c6", "PRD - Lojas": "7caa6be6-25dc-44ae-bf8f-cd2a01fea109", "PRD - Backoffice": "819a7d8f-1b0a-4121-b7dc-d001d9f109f1"}

def getRequestLimit():
    apps_V1_Api = client.AppsV1Api().list_deployment_for_all_namespaces()
    for i in apps_V1_Api.items:
        resources_requests = i.spec.template.spec.containers[0].resources.requests
        resources_limits = i.spec.template.spec.containers[0].resources.limits
        if resources_requests is not None and resources_limits is not None:
            if 'cpu' in resources_requests.keys() and 'cpu' in resources_limits.keys() and 'memory' in resources_requests.keys() and 'memory' in resources_limits.keys():
                if resources_requests["cpu"] is not None and resources_limits[
                        "cpu"] is not None and \
                    resources_limits["memory"] is not None and resources_requests[
                        "memory"] is not None:
                    if resources_requests["cpu"] == resources_limits["cpu"] or resources_limits["memory"] == \
                            resources_requests["memory"]:
                        if i.metadata.namespace != "kube-system":
                            print(
                                f'DEPLOYMENT COM REQUEST E LIMIT IGUAIS: (CPU/MEMORY): \nNamespace: {i.metadata.namespace.upper()} \nDeployment: {i.metadata.name.upper()}')
                            print(f'Request_CPU: {resources_requests["cpu"]} \n'
                                  f'Request_MEM: {resources_requests["memory"]} \n'
                                  f'Limits_CPU: {resources_limits["cpu"]} \n'
                                  f'limits_MEM: {resources_limits["memory"]}\n')
            elif 'cpu' not in resources_requests.keys() or 'cpu' not in resources_limits.keys() or 'memory' not in resources_requests.keys() or 'memory' not in resources_limits.keys():
                print(f'DEPLOYMENT NAO SETADO REQUEST OU LIMIT (CPU/MEMORY):')
                print(f'Nome do deployment: {i.metadata.name}\n')


def getHpa():
    autoscalingV1 = client.AutoscalingV1Api()
    hpaList = autoscalingV1.list_horizontal_pod_autoscaler_for_all_namespaces(
        watch=False)
    for i in hpaList.items:
        if i.spec.max_replicas <= 1:
            print(
                f'Name: {i.metadata.name} - Minimo: {i.spec.min_replicas} - Maximo: {i.spec.max_replicas} - Atual: {i.status.current_replicas}')


def getNodePools(aks, rg):
    nplist = subprocess.Popen(
        ['az', 'aks', 'nodepool', 'list', '--cluster-name', aks, '--resource-group', rg], stdout=subprocess.PIPE)
    out, err = nplist.communicate()
    nplist_json = json.loads(out)
    return nplist_json


def getAutoScaleSet():
    for sub_name, subid in subscription.items():
        get_default_cli().invoke(['account', 'set', '--subscription', subid])
        print(f'SUBSCRIPTION: {sub_name} --> SUBID: {subid}')
        akslist = subprocess.Popen(
            ['az', 'aks', 'list'], stdout=subprocess.PIPE)
        out, err = akslist.communicate()
        aks_list_json = json.loads(out)
        for cluster in aks_list_json:
            print(
                f"CLUSTER --> {cluster['name']} - RESOURCE-GROUP --> {cluster['resourceGroup']}")
            nodepools = getNodePools(cluster["name"], cluster["resourceGroup"])
            for nodepool in nodepools:
                print(
                    f'Nodepool --> {nodepool["name"]} - MinNodes --> {nodepool["minCount"]} - MaxNodes --> {nodepool["maxCount"]} - AutoScale --> {nodepool["enableAutoScaling"]}')
            print()
        print()
        print("------------------------------------------------------------------------------------------------")


def isPrd(context):
    if 'prd-admin' in str(context):
        return True
    else:
        return False


def main():
    contexts = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    context = [context['name'] for context in contexts[0]]
    # context = ["","","",""]
    index = 0
    for i in context:
        if isPrd(i):
            active_context = context[index]
            print()
            print(f'CLUSTER --> {active_context.upper()}')
            index += 1
            config.load_kube_config(context=active_context)
            # getRequestLimit()
            # getHpa()
            print()
            print("------------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    getAutoScaleSet()
