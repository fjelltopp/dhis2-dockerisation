1. Install docker for ubuntu. E.g.:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04
1. Install docker compose:
https://docs.docker.com/compose/install/#install-compose
1. Setup ssl certs with letsencrypt and nginx reverse proxy
https://certbot.eff.org/lets-encrypt/ubuntuxenial-nginx
1. Update `/etc/nginx/sites-avaiable/default`
```
server {
    listen 80;
    listen [::]:80;

    server_name dhis2-fgs-demo.fjelltopp.org; # managed by Certbot

    location / {
        #dhis2 tomcat reverse proxy setup
        proxy_set_header X-Real-IP  $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:8080;
    }

    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/dhis2-fgs-demo.fjelltopp.org/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/dhis2-fgs-demo.fjelltopp.org/privkey.pem; # managed by Certbot

}

```
1. Clone this repo:
`git clone https://github.com/fjelltopp/dhis2-dockerisation`
1. start it with
```
docker-compose -f docker-compose-country.yml -f docker-compose-ssl.yml up -d
```


Extra:

It's woth to install psql too:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
