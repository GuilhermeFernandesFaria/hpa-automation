from kubernetes import client, config
import kubernetes.client

configuration = kubernetes.client.Configuration()
resource_limit_request_notset = []
# resource_limit_request_wrongset = []


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
                            print(f'DEPLOYMENT COM REQUEST E LIMIT IGUAIS: (CPU/MEMORY): \nNamespace: {i.metadata.namespace.upper()} \nDeployment: {i.metadata.name.upper()}')
                            print(f'Request_CPU: {resources_requests["cpu"]} \n'
                                f'Request_MEM: {resources_requests["memory"]} \n'
                                f'Limits_CPU: {resources_limits["cpu"]} \n'
                                f'limits_MEM: {resources_limits["memory"]}\n')
            elif 'cpu' not in resources_requests.keys() or 'cpu' not in resources_limits.keys() or 'memory' not in resources_requests.keys() or 'memory' not in resources_limits.keys():
                print(f'DEPLOYMENT NAO SETADO REQUEST OU LIMIT (CPU/MEMORY):')
                print(f'Nome do deployment: {i.metadata.name}\n')



def getHpa():
    autoscalingV1 = client.AutoscalingV1Api()
    hpaList = autoscalingV1.list_horizontal_pod_autoscaler_for_all_namespaces(watch=False)
    for i in hpaList.items:
        print(f'{i.metadata.name} - {i.spec.min_replicas} - {i.spec.max_replicas}')


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
    # context = ["akspriv-mktplace-prd-admin","akspriv-ferrpromo-prd-admin","akspriv-mktponboarding-prd-admin","akspriv-intmktpbanqi-prd-admin"]
    index = 0
    for i in context:
        if isPrd(i):
            active_context = context[index]
            print()
            print(f'CLUSTER --> {active_context.upper()}')
            index += 1
            config.load_kube_config(context=active_context)
            getRequestLimit()
            # getHpa()
            print()
            print("------------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    main()
