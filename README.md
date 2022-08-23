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

See a sample report:

```
cat docs/sample-report.txt
```

# Additional Checks

```
python3 -m venv ./.venv
pip install -r requirements.txt
python check_best_practices.py us-east-1 eksctl-kyverno
```
