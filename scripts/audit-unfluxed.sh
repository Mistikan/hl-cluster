#!/usr/bin/env bash
# audit-unfluxed.sh
set -euo pipefail

RESOURCES=("deployments" "statefulsets" "daemonsets" "services" "configmaps" "secrets" "pods" "pvc")

flux_labels=('kustomize.toolkit.fluxcd.io/name' 'helm.toolkit.fluxcd.io/name')

for ns in $(kubectl get ns -o custom-columns=":metadata.name" --no-headers); do
  echo "🔍 Namespace: $ns"
  for res in "${RESOURCES[@]}"; do
    echo "  📦 $res:"
    kubectl get "$res" -n "$ns" -o json 2>/dev/null | \
    jq -r '.items[]? | select(
      .metadata.labels? |
      (has("'"${flux_labels[0]}"'") | not) and
      (has("'"${flux_labels[1]}"'") | not)
    ) | "    - \(.metadata.name)"' || echo "    (нет ресурсов или ошибка доступа)"
  done
done
