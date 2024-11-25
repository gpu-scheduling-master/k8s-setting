for pod in $(kubectl get pods -l app=stable-diffusion -o name -n intern); do
echo "Executing nvidia-smi on $pod:"
kubectl exec $pod -n intern -- nvidia-smi
echo "------------------------------"
done > nvidia-smi.txt