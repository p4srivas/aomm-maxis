# Installation Instructions
There are 2 phases for the AOMM FastAPI project/application installation. 
The application provides the end to end complete functionality for navigation menu, user management, login, dashboard and analysis data display and Self Assessment Form submission.

## Pre-requisites
1. Cloud environment with Kubernetes and compute / storage resources
2. A Kubernetes cluster with kubectl installed.
3. Namespace created as "nokia-aomm"
4. Helm 3 installed.
5. Access to internet (docker.io) is required from kubectl.
6. Administrative privileges on your system.

## How to Install on Kubernetes ?
Kubernetes provides a command line tool for communicating with a Kubernetes cluster's control plane, using the Kubernetes API.
This tool is named kubectl.
All installations are done using kubectl and various YAML files provided as deployment. 

### Step 1: Create dedicated namespace for Nokia AOMM project
```shell
kubectl create namespace nokia-aomm --dry-run=client -o yaml | kubectl apply -f -
```

Use the file below with modifications to create namespace in a dedicated project if needed.
```shell
cat <<EOF > aomm-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nokia-aomm
  annotations:
    field.cattle.io/projectId: local:p-hh5wr
EOF
```

Apply the updated yaml file.
```shell
kubectl apply -f aomm-namespace.yaml
```


### Step 2: Deploy PostgreSQL on Kubernetes Using a Helm Chart
Helm is a quick and easy way to deploy a PostgreSQL instance on a Kubernetes cluster. Follow the steps below to deploy PostgreSQL using Helm.

#### Add Helm Repository
Start by adding the PostgreSQL repository and updating the local repo:
1. Search Artifact Hub for a PostgreSQL Helm chart. Add the chart's repository to the local Helm installation. For example, if using the official Bitnami PostgreSQL repo URL, run:
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
```

2. Update the local repositories:
```shell
helm repo update
```

#### Install Helm Chart for postgres DB
3. Run the helm command. Ensure that the storage class setting is correct, e.g. cinder etc.
```shell
helm install --namespace nokia-aomm aomm \
	--set image.tag=16.1.0-debian-11-r4 \
	--set postgresqlDataDir=/var/lib/postgresql/data/pgdata \
	--set primary.persistence.mountPath=/var/lib/postgresql/data \
	--set primary.persistence.storageClass="standard" \
	--set primary.persistence.size=8Gi \
	--set primary.persistentVolumeClaimRetentionPolicy.enabled=true \
	--set primary.persistentVolumeClaimRetentionPolicy.whenScaled=Retain \
	--set primary.persistentVolumeClaimRetentionPolicy.whenDeleted=Delete \
	--set primary.initdb.postgresqlWalDir=/var/lib/postgresql/data/pgdata/pg_wal \
    	--set primary.resources.requests.memory="2Gi" \
    	--set primary.resources.requests.cpu="1" \
    	--set primary.resources.limits.memory="4Gi" \
    	--set primary.resources.limits.cpu="2" \
	oci://registry-1.docker.io/bitnamicharts/postgresql 
```

#### Get postgres user password and store it seprately in a secured manner.
Get password for default "postgres" user
```shell
kubectl get secret --namespace nokia-aomm aomm-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d
```

```shell
helm uninstall --namespace nokia-aomm aomm
```

### Step 3: Deploy pgAdmin in Kubernetes
pgAdmin has long had a container distribution. This step is only necessary if any 
local deployment of pgAmin on Windows etc. is not able to access the postgres DB 
in Kubernetes cloud.

There are 4 steps, secret, configmap, service and statefulset.

Note that all the YAML below could be in a single file, however it is split up into multiple files for convenience.

1. Secret
This is a way of storing sensitive information in Kubernetes for use as part of whatever is being deployed. In the case of pgAdmin, we'll use it to store the initial password that will be set for the administrator. This will create a secret with the name pgadmin. The password is simply base64 encoded (in this case, it's *****).
Create the YAML file.
```shell
cat <<EOF > pgadmin-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: pgadmin-secret
type: Opaque
data:
  pgadmin-default-password: bXlwd2Q=
EOF
```

Apply the YAML file.
```shell
kubectl --namespace nokia-aomm apply -f pgadmin-secret.yaml
```

2. ConfigMap
Next create a configuration file for pgAdmin. The ConfigMap is used to inject a JSON file that contains a list of servers to register for use.
Set the IP address of the host (edge node of Kubernetes cluster). 
Create the YAML file.
```shell
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
           "Host": "34.118.225.226",
           "SSLMode": "prefer",
           "MaintenanceDB": "postgres"
         }
       }
   }
EOF
```

Apply the YAML file.
```shell
kubectl --namespace nokia-aomm apply -f pgadmin-configmap.yaml
```

3. Deployment
The final piece of the puzzle is a pgAdmin4 deployment.  
Create YAML file
```shell
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
```

Apply the YAML
```shell
kubectl --namespace nokia-aomm apply -f pgadmin-deploy.yaml
```

4. Service
A service in Kubernetes is an abstract way to describe a logical set of pods (containing one or more containers) and a policy by which they can be accessed.
Create the YAML file.
```shell
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
```

Apply the YAML file
```shell
kubectl --namespace nokia-aomm apply -f pgadmin-service.yaml
```


### Step 4: Setup connection to postgres in pgAdmin

### Step 5: Download aomm-data SQL scripts 
Using authorized access to Nokia Sharenet, download the two scripts for database creation and schema population.

### Step 6: Create database in PostgreSQL using pgAdmin tool.
Open pgAdmin and create local database "aomm-data"

Open db-query window in pgAdmin after selecting the database "aomm-data".

Copy and paste the content of file \fastapi-aomm\postgres\setup_db.sql to the query window and execute.

Next, copy and paste the content of file \fastapi-aomm\postgres\setup_schema.sql to the query window and execute.

Voila! Database schema is created. 

### Step 7: Add data to the tables with a one-time utility: aomm-setup job YAML
1. First create a aomm-configmap after modifying the values below for DB_HOST, DB_PORT (if not 5432).
```shell
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
```

2. Apply the aomm-setup configmap YAML
```shell
kubectl --namespace nokia-aomm apply -f nokia-aomm-config.yaml
```

3. Check if the values are correctly set.
```shell
kubectl --namespace nokia-aomm describe configmap  aomm-configmap
```

4. Run the aomm-setup job YAML
```shell
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
```

5. Apply the aomm-setup Job YAML
```shell
kubectl --namespace nokia-aomm apply -f create-aomm-setup.yaml
```

6. Test if data is populated.
After the job is successfullt completed, check from PGAdmin query window 
if data is populated by running the following query on database aomm-data
```sql
SELECT * FROM public.operation_sub_group_map;
```
Sample data for operations and operation_sub_group and other data is populated.


### Step 8: Install Nokia AOMM application
1. Use the same configmap YAML file created in step 7(1) above.
Verify if the values are correctly set.
```shell
kubectl --namespace nokia-aomm describe configmap  aomm-configmap
```

2. In case not set or deleted, repeat the process to create the configmap again.
Remember to update the values below for DB_HOST, DB_PORT (if not 5432). 
```shell
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
```

3. Apply the aomm-setup configmap YAML only if step 8(2) is executed.
```shell
kubectl --namespace nokia-aomm apply -f nokia-aomm-config.yaml
```

2. Create fastapi-aomm deployment YAML
```shell
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
```

Apply the deployment YAML file
```shell
kubectl --namespace nokia-aomm apply -f create-fastapi-aomm.yaml
```

3. Create service YAML
```shell
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
```

Apply the service YAML file
```shell
kubectl --namespace nokia-aomm apply -f nokia-aomm-service.yaml
```

Create new user by going to URL http://aomm-app-url-host:aomm-nodeport/

New admin user is created using admin user credentials.

The password is stored in encrypted format (one way ecryption) and is only known to the actual user.