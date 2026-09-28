# Talos

The cluster is managed with [topf](https://github.com/postfinance/topf): `topf.yaml` describes
the cluster and nodes, `secrets.sops.yaml` is the SOPS-encrypted Talos secrets bundle, and the
installer image is built from `factory` + `schematic.yaml` + `talosVersion`.

## Patch Directories

Strategic merge patches are applied in lexicographic order within each directory:

- `all/`: patches applied to every node
- `control-plane/`: patches applied to control-plane nodes
- `worker/`: patches applied to worker nodes
- `node/<host>/`: patches applied to the node with the matching `host` from `topf.yaml`

Files ending in `.tpl` are rendered as Go templates (`{{ .Node.Host }}`, `{{ .Data.* }}`).

## Tasks

- `task talos:apply DRY_RUN=true` — diff the generated config against the running nodes
- `task talos:apply` — apply the config
- `task talos:upgrade` — upgrade Talos to `talosVersion`
- `task talos:upgrade-k8s` — upgrade Kubernetes to `kubernetesVersion`
- `task talos:render` — write full machine configs to `output/` (contains secrets)
