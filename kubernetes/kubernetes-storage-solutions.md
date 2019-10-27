# Working with different storage solutions in your cluster

## Importing External Services

It is possible to represent an external service in kubernetes, one caveat is there are no health checks.

Using a DNS name

```yaml
kind: Service
apiVersion: v1
metadata:
   name: external-database
spec:
   type: ExternalName
   externalName: database.company.com
```

Using an IP address

```yaml
kind: Service
apiVersion: v1
metadata:
   name: external-ip-database
__________________________
kind: Endpoints
apiVersion: v1
metadata:
   name: external-ip-database
subsets:
   - addresses:
      # for more than one IP you can populate this area with an array
      - ip: 192.168.0.1
      ports:
      - port: 3306
```
