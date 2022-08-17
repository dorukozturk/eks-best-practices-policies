# Prerequisites

- Install Kyverno by following [this](https://kyverno.io/docs/installation/).
- kube-system namespace is ignored by default so we have to edit the kyverno configmap.
```
kubectl edit configmap kyverno -n kyerno
```

and remove:

```yaml
[*,kube-system,*]
```
from the configmap


# Instructions

Apply policies:

```
kubectl apply -f security/
```

Check out the report:
```
kubectl describe polr -A | grep -i "Result: \+fail" -B10
```

Some sample test cases to trigger the fails:

```
kubectl apply -f tests/
```