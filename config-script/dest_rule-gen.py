import yaml
import subprocess

# Define namespace and service name
namespace = "intern"
service_name = "sd-service"
destination_rule_name = "sd-api-dest"

# Get all pod names in the namespace
pods_output = subprocess.check_output(
    ["kubectl", "get", "pods", "-n", namespace, "-o", "jsonpath={.items[*].metadata.name}"]
).decode("utf-8")
pod_names = pods_output.split()

# Build subsets based on pod names
subsets = []
for pod_name in pod_names:
    subsets.append({
        "name": pod_name,
        "labels": {
            "pod": pod_name
        }
    })

# Define DestinationRule YAML structure
destination_rule = {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "DestinationRule",
    "metadata": {
        "name": destination_rule_name,
        "namespace": namespace,
    },
    "spec": {
        "host": service_name,
        "subsets": subsets,
    }
}

# Save the YAML to a file
output_file = "destination-rule.yaml"
with open(output_file, "w") as f:
    yaml.dump(destination_rule, f, default_flow_style=False)

print(f"DestinationRule YAML file generated: {output_file}")
