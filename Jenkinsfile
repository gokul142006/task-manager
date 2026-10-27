stage('Deploy to Kubernetes') {
    steps {
        withCredentials([
            string(
                credentialsId: 'k8s-token',
                variable: 'K8S_TOKEN'
            )
        ]) {
            sh '''
                set +x

                kubectl \
                  --server=https://host.docker.internal:52844 \
                  --token="$K8S_TOKEN" \
                  --insecure-skip-tls-verify=true \
                  apply -f k8s/deployment.yaml

                kubectl \
                  --server=https://host.docker.internal:52844 \
                  --token="$K8S_TOKEN" \
                  --insecure-skip-tls-verify=true \
                  apply -f k8s/service.yaml
            '''
        }
    }
}
