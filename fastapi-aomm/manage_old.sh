## Remember to set correct mapping for database in database.py and helper.py!!!

cat <<EOF > create-fastapi-aomm.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-aomm
  labels:
    app: fastapi-aomm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi-aomm
  template:
    metadata:
      labels:
        app: fastapi-aomm
    spec:
      containers:
      - name: fastapi-aomm
        image: p4srivas/fastapi-aomm:v1.0109
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: DB_HOST
        - name: DB_PORT
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: DB_PORT
        - name: ROOT_PATH
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: ROOT_PATH
        - name: POSTGRES_PWD
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: POSTGRES_PWD
      restartPolicy: Always
EOF

kubectl --namespace managedservices-mas-maxis create -f create-fastapi-aomm.yaml

kubectl --namespace managedservices-mas-maxis logs fastapi-aomm

kubectl --namespace managedservices-mas-maxis delete deployment fastapi-aomm

kubectl --namespace managedservices-mas-maxis scale --replicas=0 deployment/fastapi-aomm
kubectl --namespace managedservices-mas-maxis scale --replicas=1 deployment/fastapi-aomm

cat <<EOF > fastapi-aomm-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-aomm
  labels:
    app: fastapi-aomm
spec:
  type: ClusterIP
  ports:
   - port: 8000
  selector:
   app: fastapi-aomm
EOF

kubectl --namespace managedservices-mas-maxis apply -f fastapi-aomm-service.yaml

cat <<EOF > nokia-aomm-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aomm-configmap
data:
  DB_HOST: "10.255.63.242"
  DB_PORT: "5432"
  ROOT_PATH: "/usr/src/app/"
  POSTGRES_PWD: "Je8e39bOeg"
EOF

kubectl --namespace managedservices-mas-maxis apply -f nokia-aomm-config.yaml

kubectl --namespace managedservices-mas-maxis describe configmap  aomm-configmap




cat <<EOF > aomm-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nokia-aomm
  annotations:
    field.cattle.io/projectId: local:p-rk7bw
EOF

kubectl apply -f aomm-namespace.yaml


cat <<EOF > pgadmin-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: pgadmin-secret
type: Opaque
data:
  pgadmin-default-password: bXlwd2Q=
EOF

kubectl --namespace nokia-aomm apply -f pgadmin-secret.yaml

cat <<EOF > pgadmin-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pgadmin
spec:
  selector:
   matchLabels:
    app: pgadmin
  replicas: 1
  template:
    metadata:
      labels:
        app: pgadmin
    spec:
      containers:
        - name: pgadmin4
          image: dpage/pgadmin4:8.4
          env:
            - name: PGADMIN_DEFAULT_EMAIL
              value: "prashant.7.srivastava@nokia.com"
            - name: PGADMIN_DEFAULT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: pgadmin-secret
                  key: pgadmin-default-password
            - name: PGADMIN_PORT
              value: "80"
          ports:
          - name: http
            containerPort: 80
            name: pgadminport
EOF

kubectl --namespace nokia-aomm apply -f pgadmin-deploy.yaml

cat <<EOF > pgadmin-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: pgadmin
  labels:
    app: pgadmin
spec:
  selector:
    app: pgadmin
  type: NodePort
  ports:
    - port: 80
      nodePort: 30200
EOF

kubectl --namespace nokia-aomm apply -f pgadmin-service.yaml

























cat <<EOF > create-nokia-aomm.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nokia-aomm
  labels:
    app: nokia-aomm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nokia-aomm
  template:
    metadata:
      labels:
        app: nokia-aomm
    spec:
      containers:
      - name: nokia-aomm
        image: p4srivas/fastapi-aomm:v1.0108
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: DB_HOST
        - name: DB_PORT
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: DB_PORT
        - name: ROOT_PATH
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: ROOT_PATH
        - name: POSTGRES_PWD
          valueFrom:
            configMapKeyRef:
              name: aomm-configmap
              key: POSTGRES_PWD                            
      restartPolicy: Always
EOF

kubectl --namespace managedservices-mas-maxis apply -f create-nokia-aomm.yaml

kubectl --namespace managedservices-mas-maxis delete deployment nokia-aomm

cat <<EOF > nokia-aomm-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nokia-aomm
  labels:
    app: nokia-aomm
spec:
  type: ClusterIP
  ports:
   - port: 8000
  selector:
   app: nokia-aomm
EOF

kubectl --namespace managedservices-mas-maxis apply -f nokia-aomm-service.yaml
kubectl --namespace managedservices-mas-maxis delete service nokia-aomm