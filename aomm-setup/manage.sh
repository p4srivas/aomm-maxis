
kubectl create namespace nokia-aomm --dry-run=client -o yaml | kubectl apply -f -
kubectl annotate --overwrite namespace nokia-aomm field.cattle.io/projectId: local:p-hh5wr

cat <<EOF > aomm-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nokia-aomm
  annotations:
    field.cattle.io/projectId: local:p-hh5wr
EOF

kubectl apply -f aomm-namespace.yaml

helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update

helm install --namespace nokia-aomm aomm \
	--set image.tag=16.1.0-debian-11-r4 \
	--set postgresqlDataDir=/var/lib/postgresql/data/pgdata \
	--set primary.persistence.mountPath=/var/lib/postgresql/data \
	--set primary.persistence.storageClass="cinder-csi" \
	--set primary.persistence.size=20Gi \
	--set primary.persistentVolumeClaimRetentionPolicy.enabled=true \
	--set primary.persistentVolumeClaimRetentionPolicy.whenScaled=Retain \
	--set primary.persistentVolumeClaimRetentionPolicy.whenDeleted=Delete \
	--set primary.initdb.postgresqlWalDir=/var/lib/postgresql/data/pgdata/pg_wal \
    	--set primary.resources.requests.memory="2Gi" \
    	--set primary.resources.requests.cpu="2" \
    	--set primary.resources.limits.memory="4Gi" \
    	--set primary.resources.limits.cpu="4" \
	oci://registry-1.docker.io/bitnamicharts/postgresql 





helm uninstall --namespace nokia-aomm aomm

kubectl get secret --namespace nokia-aomm aomm-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
Klccr055Ot

kubectl get secret --namespace nokia-aomm postgres-aomm-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
TPQdZ7keCJ



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

cat <<EOF > pgadmin-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
 name: pgadmin-config
data:
 servers.json: |
   {
       "Servers": {
         "1": {
           "Name": "aomm",
           "Group": "Servers",
           "Port": 5432,
           "Username": "postgres",
           "Host": "10.255.8.206",
           "SSLMode": "prefer",
           "MaintenanceDB": "postgres"
         }
       }
   }
EOF

kubectl --namespace nokia-aomm apply -f pgadmin-configmap.yaml

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
            value: admin@admin.com
          - name: PGADMIN_DEFAULT_PASSWORD
            valueFrom:
              secretKeyRef:
                name: pgadmin-secret
                key: pgadmin-default-password
          ports:
          - name: http
            containerPort: 80
            protocol: TCP
          volumeMounts:
          - name: pgadmin-config
            mountPath: /pgadmin4/servers.json
            subPath: servers.json
            readOnly: true
      volumes:
      - name: pgadmin-config
        configMap:
          name: pgadmin-config
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
    - protocol: TCP
      port: 80
      nodePort: 30200
      targetPort: http
EOF

kubectl --namespace nokia-aomm apply -f pgadmin-service.yaml


## Open pgAdmin and create local database "aomm_data"

## Open db-query window in pgAdmin after selecting the database "aomm_data".

## Copy and paste the content of file \fastapi-aomm\postgres\setup_db.sql to the query window and execute.

## Next, copy and paste the content of file \fastapi-aomm\postgres\setup_schema.sql to the query window and execute.

## Voila! Database schema is created. 


cat <<EOF > nokia-aomm-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aomm-configmap
data:
  DB_HOST: "10.255.36.107"
  DB_PORT: "5432"
  ROOT_PATH: "/usr/src/app/"
  POSTGRES_PWD: "TPQdZ7keCJ"
EOF

kubectl --namespace nokia-aomm apply -f nokia-aomm-config.yaml

kubectl --namespace nokia-aomm describe configmap  aomm-configmap

cat <<EOF > create-aomm-setup.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: aomm-setup
spec:
  template:
    spec:
      containers:
      - name: aomm-setup
        image: p4srivas/aomm-setup:v1.0012e
        command: ["python", "setup_aomm.py"] 
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
      restartPolicy: Never
EOF

kubectl --namespace nokia-aomm apply -f create-aomm-setup.yaml

kubectl --namespace nokia-aomm delete job aomm-setup

cat <<EOF > create-nokia-aomm.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aomm-fastapi
  labels:
    app: aomm-fastapi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aomm-fastapi
  template:
    metadata:
      labels:
        app: aomm-fastapi
    spec:
      containers:
      - name: aomm-fastapi
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

kubectl --namespace nokia-aomm apply -f create-nokia-aomm.yaml

kubectl --namespace nokia-aomm delete deployment aomm-fastapi

cat <<EOF > nokia-aomm-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: aomm-fastapi
  labels:
    app: aomm-fastapi
spec:
  selector:
    app: aomm-fastapi
  type: NodePort
  ports:
    - port: 8000
      nodePort: 30500
EOF

kubectl --namespace nokia-aomm apply -f nokia-aomm-service.yaml
kubectl --namespace nokia-aomm delete service aomm-fastapi