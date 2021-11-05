from kubernetes import client, config
import kubernetes.client

configuration = kubernetes.client.Configuration()


def getHpa():
    autoscalingV1 = client.AutoscalingV1Api()
    hpaList = autoscalingV1.list_horizontal_pod_autoscaler_for_all_namespaces(watch=False)
    for i in hpaList.items:
        print(f'Name: {i.metadata.name} - MinPods: {i.spec.min_replicas} - MaxPods: {i.spec.max_replicas} - Replicas: {i.status.current_replicas} -'
              f' Namespace: {i.metadata.namespace} ')

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
    # context = [context['name'] for context in contexts[0]]
    context = ["akspriv-entregamais-prd-admin","akspriv-envias-prd-admin","akspriv-logreversa-prd-admin","akspriv-oferta-prd-admin", "akspriv-retira-prd-admin"]
    index = 0
    for i in context:
        if isPrd(i):
            active_context = context[index]
            print(active_context)
            index += 1
            config.load_kube_config(context=active_context)
            getHpa()
            print()


if __name__ == '__main__':

    main()
