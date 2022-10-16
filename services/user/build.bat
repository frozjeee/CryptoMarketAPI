docker build -t frozje/user-service . --no-cache
kubectl rollout restart deployment/user-service
PAUSE