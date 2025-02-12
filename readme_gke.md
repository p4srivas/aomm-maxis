# Installation Instructions
There are 2 phases for the AOMM FastAPI project/application installation. 
The application provides the end to end complete functionality for navigation menu, user management, login, dashboard and analysis data display and Self Assessment Form submission.

## Pre-requisites
1. GKE API is enabled
2. A Kubernetes cluster with kubectl installed.
3. Namespace created as "aomm"
4. Administrative privileges on your system.

## How to Install on Kubernetes ?
Kubernetes provides a command line tool for communicating with a Kubernetes cluster's control plane, using the Kubernetes API.
This tool is named kubectl.
All installations are done using kubectl and various YAML files provided as deployment. 


Connect to the GKE cluster.
```shell
gcloud container clusters get-credentials cluster-2 --zone us-central1-a --project aomm-446714
```

### Step 1: Create dedicated namespace for Nokia AOMM project
```shell
kubectl create namespace aomm --dry-run=client -o yaml | kubectl apply -f -
```

### Step 2: Deploy PostgreSQL on Google Kubernetes Engine Using Marketplace
Create postgres instance with name "aomm-1"
Enable expose public IP
follow instructions. Select the namespace as aomm.
Once installed, note the password and public IP


#### Get postgres user password and store it seprately in a secured manner.
Get password for default "postgres" user
```shell
kubectl get secret --namespace aomm aomm-1-secret -o jsonpath="{.data.password}" | base64 -d
```

Output with password 6cprRHVgwrLf
```shell
psrivastava_noida@cloudshell:~ (aomm-446714)$ kubectl get secret --namespace aomm aomm-1-secret -o jsonpath="{.data.password}" | base64 -d
6cprRHVgwrLfpsrivastava_noida@cloudshell:~ (aomm-446714)$
```



### Step 3: Setup connection to postgres in local pgAdmin
Use the postgres user password and postgres public IP, port 5432 to connect.

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
  DB_HOST: "34.122.253.56"
  DB_PORT: "5432"
  ROOT_PATH: "/usr/src/app/"
  POSTGRES_PWD: "6cprRHVgwrLf"
EOF
```

2. Apply the aomm-setup configmap YAML
```shell
kubectl --namespace aomm apply -f nokia-aomm-config.yaml
```

3. Check if the values are correctly set.
```shell
kubectl --namespace aomm describe configmap  aomm-configmap
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
kubectl --namespace aomm apply -f create-aomm-setup.yaml
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
kubectl --namespace aomm describe configmap  aomm-configmap
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
  DB_HOST: "34.122.253.56"
  DB_PORT: "5432"
  ROOT_PATH: "/usr/src/app/"
  POSTGRES_PWD: "6cprRHVgwrLf"
EOF
```

3. Apply the aomm-setup configmap YAML only if step 8(2) is executed.
```shell
kubectl --namespace aomm apply -f nokia-aomm-config.yaml
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
kubectl --namespace aomm apply -f create-nokia-aomm.yaml
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
  type: ClusterIP
  ports:
    - port: 8000
EOF
```

Apply the service YAML file
```shell
kubectl --namespace aomm apply -f nokia-aomm-service.yaml
```

```shell
kubectl expose --namespace aomm deployment aomm-fastapi --name=aomm-fastapi-expose --type=LoadBalancer --port 80 --target-port 8000
```

Create new user by going to URL http://aomm-app-url-host:aomm-nodeport/

New admin user is created using admin user credentials.

The password is stored in encrypted format (one way ecryption) and is only known to the actual user.