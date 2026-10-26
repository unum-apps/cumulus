# cumulus

Pain cycle app. Record events and bucket them.

# Development

Needs Docker, [kubectx](https://formulae.brew.sh/formula/kubectx), [Tilt](https://docs.tilt.dev/install.html) and a kind cluster with MySQL in the `mysql` namespace.

- `make up` - Runs Tilt against the `kind-us` cluster (`make up CONTEXT=kind-them` to use another). GUI is http://localhost:6465, API http://localhost:16465, Tilt http://localhost:7635
- `make down` - Removes everything from the cluster
