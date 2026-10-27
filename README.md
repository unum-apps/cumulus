# cumulus

Pain cycle app. Record events and bucket them.

# Install

To use this app's interface (`unum_cumulus`, which lists the models it owns) from another app, list it in requirements.txt as:

```
git+ssh://git@github.com/unum-apps/cumulus.git@0.1.0#egg=unum-cumulus
```

Use a version that's been tagged. Jenkins tags the version in `VERSION` on every merge to main, or use `make tag`.

# Development

Needs Docker, [kubectx](https://formulae.brew.sh/formula/kubectx), [Tilt](https://docs.tilt.dev/install.html) and a kind cluster with MySQL in the `mysql` namespace.

- `make up` - Runs Tilt against the `docker-desktop` cluster. GUI is http://localhost:6465, API http://localhost:16465, Tilt http://localhost:7635
- `make down` - Removes everything from the cluster
- `make setup` - Verifies that this repo can be installed as a module by other apps
- `make tag` - Tags this repo with the version in `VERSION` and pushes the tag, and does nothing if it's already there
- `make untag` - Undoes the tagging
