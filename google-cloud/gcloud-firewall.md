# Working with Gcloud's firewall

Configure firewall to allow tcp traffic on port 80

```sh
gcloud compute firewall-rules create www-firewall --allow tcp:80
```

