k8s_yaml(kustomize('kubernetes/tilt'))

k8s_resource(
  objects=['cumulus:namespace'],
  new_name='namespace'
)

local_resource(
    name='config', resource_deps=['namespace'],
    cmd='kubectl -n cumulus create configmap config --from-file config/ --dry-run=client -o yaml | kubectl apply -f -'
)

local_resource(
    name='secret', resource_deps=['namespace'],
    cmd='kubectl -n cumulus create secret generic secret --from-file secret/ --dry-run=client -o yaml | kubectl apply -f -'
)

# api

docker_build('unum-apps-cumulus-api', './api')
k8s_resource('api', port_forwards=['16465:80', '16433:5678'], resource_deps=['secret'])

# gui

docker_build('unum-apps-cumulus-gui', './gui')
k8s_resource('gui', port_forwards=['6465:80'], resource_deps=['api'])
