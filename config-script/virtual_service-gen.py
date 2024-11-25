import yaml
import subprocess

# Define constants
namespace = "intern"
service_name = "sd-service"
virtual_service_name = "sd-api-virtual"
gateway_name = "sd-gateway"
host_uri = "/gen-img"
port_number = 8000

# Get all pod names in the namespace
pods_output = subprocess.check_output(
    ["kubectl", "get", "pods", "-n", namespace, "-o", "jsonpath={.items[*].metadata.name}"]
).decode("utf-8")
pod_names = pods_output.split()

# Calculate weight
num_pods = len(pod_names)
weight_per_pod = max(1, 100 // num_pods)

# Build VirtualService YAML structure
virtual_service = {
    "apiVersion": "networking.istio.io/v1alpha3",
    "kind": "VirtualService",
    "metadata": {
        "name": virtual_service_name,
        "namespace": namespace,
    },
    "spec": {
        "hosts": ["*"],
        "gateways": [f"{namespace}/{gateway_name}"],
        "http": [
            {
                "match": [{"uri": {"exact": host_uri}}],
                "route": [
                    {
                        "destination": {
                            "host": service_name,
                            "subset": pod_name,
                            "port": {"number": port_number},
                        },
                        "weight": weight_per_pod,
                    }
                    for pod_name in pod_names
                ],
            }
        ],
    },
}

# Build Service YAML structure
service = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "name": service_name,
        "namespace": namespace,
        "labels": {
            "app": "stable-diffusion",
            "service": "stable-diffusion",
        },
    },
    "spec": {
        "ports": [
            {
                "port": port_number,
                "name": "http",
            }
        ],
        "selector": {
            "app": "stable-diffusion",
        },
    },
}

# Save the YAML to a file
output_file = "istio_virtual_service_and_service.yaml"
with open(output_file, "w") as f:
    yaml.dump_all([service, virtual_service], f, default_flow_style=False)

print(f"YAML file generated: {output_file}")
