# Working with Persistent Volumes

Kubernetes has multiple drivers to hook into persistent storage including (nfs, azure, awsElasticBlockStore, gcePersistentDisk)

Example of creating nfs volume

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
   name: database
   labels:
      # used by the volume claim to select the volume
      volume: my-volume
spec:
   accessModes:
   - ReadWriteMany
   capacity:
      storage: 1Gi
   # substitute this value with any of the available types (nfs, azure, awsElasticBlockStore, gcePersistentDisk)
   nfs:
      server: 192.168.0.1
      path: "/exports"
```

Then apply the object

```sh
kubectl apply -f <nfs-volume.yaml>
```

To claim that newly created nfs value for a Pod

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
   name: database
spec:
   accessModes:
   - ReadWriteMany
   resources:
      requests:
         storage: 1Gi
   selector:
      # this value uses the selector to match the volume
      matchLabels:
         volume: my-volume
```

MySQL example with ReplicaSet and Reference to PersistenVolumeClaim

```yaml
apiVersion: extensions/v1
kind: ReplicaSet
metadata:
   name: mysql
   # labels so that we can bind a Service to this Pod
   labels:
      app: mysql
spec:
   replicas: 1
   selector:
      matchLabels:
      app: mysql
   template:
      metadata:
         labels:
            app: mysql
   spec:
      containers:
         - name: database
            image: mysql
            resources:
               requests:
                  cpu: 1
                  memory: 2Gi
            env:
            # Environment variables are not a best practice for security,
            # but we're using them here for brevity in the example.
            # See Chapter 11 for better options. Kubernetes: Up and Running
            - name: MYSQL_ROOT_PASSWORD
               value: some-password-here
            livenessProbe:
               tcpSocket:
                  port: 3306
            ports:
            - containerPort: 3306
            volumeMounts:
               - name: database
                  # /var/lib/mysql is where MySQL stores its databases
                  mountPath: "/var/lib/mysql"
      volumes:
         - name: database
            persistentVolumeClaim:
               claimName: database
```

## Dynamic Volume Provisioning

To create a dynamic volume, create a StorageClass.
For example to create a default StorageClass that automatically provisions disk objects on the Microsoft Azure Platform

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
   name: default
   annotations:
      storageclass.beta.kubernetes.io/is-default-class: "true"
   labels:
      kubernetes.io/cluster-service: "true"
provisioner: kubernetes.io/azure-disk
```

Once a storage class has been created for the cluster you can refer to this storage class in your persistent volume claim rather than refering to any specific volume.

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
   name: my-claim
   annotations:
      # this is what links the storage-class to the volume claim
      volume.beta.kubernetes.io/storage-class: default
spec:
   accessModes:
   - ReadWriteOnce
   resources:
      requests:
         storage: 10Gi
```

## Kubernetes StatefulSets

StatefulSets are replicated groups of Pods, similar to ReplicaSets but have unique qualities:

- each replica gets a consistent hostname with a unique index ( app-0, app-1, db-0, db-1)
- each replica is created in order from the lowest to the highest, blocking while the previous index health and availability is checked
- when a StatefulSet is deleted, each of the managed replica Pods is deleted from the highest index to the lowest, this also applies to scaling down the replicas

When referencing volumes with StatefulSets you cannot simply reference a persistent colume claim.
Instead you need a persisten volume claim template, similar to a Pod template except instead of creating Pods it creates volume claims.

A volume claim template example

```yaml
volumeClaimTemplates:
- metadata:
      name: database
      annotations:
      volume.alpha.kubernetes.io/storage-class: anything
spec:
   accessModes: [ "ReadWriteOnce" ]
   resources:
      requests:
         storage: 100Gi
```

A StatefulSet example with mongoDB and automation script

```yaml
# the order of this yaml config is Service, ConfigMap, StatefulSet
# service
apiVersion: v1
kind: Service
metadata:
   name: mongo
spec:
   ports:
   - port: 27017
      name: peer
   clusterIP: None
   selector:
      app: mongo
---
# configmap
apiVersion: v1
kind: ConfigMap
metadata:
   name: mongo-init
data:
   init.sh: |
      #!/bin/bash
      # Need to wait for the readiness health check to pass so that the
      # mongo names resolve. This is kind of wonky.
      until ping -c 1 ${HOSTNAME}.mongo; do
         echo "waiting for DNS (${HOSTNAME}.mongo)..."
         sleep 2
      done

      until /usr/bin/mongo --eval 'printjson(db.serverStatus())'; do
         echo "connecting to local mongo..."
         sleep 2
      done

      echo "connected to local."
      HOST=mongo-0.mongo:27017
      until /usr/bin/mongo --host=${HOST} --eval 'printjson(db.serverStatus())'; do
         echo "connecting to remote mongo..."
         sleep 2
      done

      echo "connected to remote." 
      if [[ "${HOSTNAME}" != 'mongo-0' ]]; then
         until /usr/bin/mongo --host=${HOST} --eval="printjson(rs.status())" \
               | grep -v "no replset config has been received"; do
            echo "waiting for replication set initialization"
            sleep 2
         done
         echo "adding self to mongo-0"
         /usr/bin/mongo --host=${HOST} \
         --eval="printjson(rs.add('${HOSTNAME}.mongo'))"
      fi

      if [[ "${HOSTNAME}" == 'mongo-0' ]]; then
         echo "initializing replica set"
         /usr/bin/mongo --eval="printjson(rs.initiate(\
            {'_id': 'rs0', 'members': [{'_id': 0, \
            'host': 'mongo-0.mongo:27017'}]}))"
      fi
      echo "initialized"

      while true; do
         sleep 3600
      done
---
# StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
   name: mongo
spec:
   serviceName: "mongo"
   replicas: 3
   template:
   metadata:
      labels:
         app: mongo
   spec:
      containers:
      - name: mongodb
         image: mongo:3.4.1
         command:
         - mongod
         - --replSet
         - rs0
         ports:
         - containerPort: 27017
            name: web
         livenessProbe:
            exec:
               command:
               - /usr/bin/mongo
               - --eval
               - db.serverStatus()
            initialDelaySeconds: 10
            timeoutSeconds: 10
   # This container initializes the mongodb server, then sleeps.
   - name: init-mongo
      image: mongo:3.4.1
      command:
      - bash
      - /config/init.sh
      volumeMounts:
      - name: config
         mountPath: /config
   volumes:
      - name: config
         configMap:
            name: "mongo-init"
   # utilizing a persistent volume claim template
   volumeClaimTemplates:
   - metadata:
         name: database
         annotations:
            volume.alpha.kubernetes.io/storage-class: anything
   spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
         requests:
            storage: 100Gi
```