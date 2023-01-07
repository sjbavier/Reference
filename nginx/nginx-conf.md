# Sample nginx conf

```conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
worker_connections 1024;
}

http {
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
'$status $body_bytes_sent "$http_referer" '
'"$http_user_agent" "$http_x_forwarded_for"';

access_log  /var/log/nginx/access.log  main;

sendfile            on;
tcp_nopush          on;
tcp_nodelay         on;
keepalive_timeout   65;
types_hash_max_size 2048;
server_tokens off;

# https://developer.mozilla.org/en-US/docs/HTTP/X-Frame-Options
add_header X-Frame-Options SAMEORIGIN;
add_header X-Content-Type-Options nosniff;

# https://www.owasp.org/index.php/List_of_useful_HTTP-headers
add_header X-XSS-Protection "1; mode=block";

gzip on;
gzip_disable "msie6";

include             /etc/nginx/mime.types;
default_type        application/octet-stream;

# Load modular configuration files from the /etc/nginx/conf.d directory.
# See http://nginx.org/en/docs/ngx_core_module.html#include
# for more information.
include /etc/nginx/conf.d/*.conf;

server {
listen 80;
server_name $SERVER_NAME;
rewrite ^ https://$server_name$request_uri? permanent;  # enforce https
}

server {
  listen          443 ssl;
  ssl_prefer_server_ciphers on;
  ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
  ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";
  ssl_certificate     /etc/nginx/ssl/wildcard.crt;
  ssl_certificate_key /etc/nginx/ssl/wildcard.key;

  server_name  $SERVER_NAME;

  access_log  /var/log/nginx/$SERVER_NAME.access.log;

  root /var/www/html/;

  keepalive_timeout 60;

  # accessing root go to index
  location / {
  try_files $uri /index.html;
  }

  # gzip static files
  location ~ ^/static/ {
  gzip_static on;
  expires max;
  add_header Cache-Control public;
  add_header Last-Modified "";
  add_header ETag "";
  }

  # don't serve hidden files
  location ~ /\. {
  return 404;
  access_log off;
  log_not_found off;
  }

  # try to load favicon else code 204
  location = /favicon.ico {
  try_files /favicon.ico = 204;
  access_log off;
  log_not_found off;
  }

  location /$PATH_TO_PROXY {
    proxy_pass      http://127.0.0.1:3003/$PATH_TO_PROXY;
    proxy_redirect  off;
    proxy_set_header   Host             $host;
    proxy_set_header X-Forwarded-Server $host;
    proxy_set_header   X-Real-IP        $remote_addr;
    proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    client_max_body_size       50m;
    client_body_buffer_size    128k;#
    proxy_connect_timeout      60;
    proxy_send_timeout         60;
    proxy_read_timeout         60;
    proxy_buffer_size          4k;
    proxy_buffers              4 32k;
    proxy_busy_buffers_size    64k;
    proxy_temp_file_write_size 64k;
  }

  error_page  404  /404.html;

  # redirect server error pages to the static page /50x.html
  error_page   500 502 503 504  /50x.html;
  location = /50x.html {
  root   /var/www/nginx-default;
}
}
}
```
