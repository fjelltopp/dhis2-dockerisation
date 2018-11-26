1. Install docker for ubuntu. E.g.:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04
1. Install docker compose:
https://docs.docker.com/compose/install/#install-compose
1. Setup ssl certs with letsencrypt and nginx reverse proxy
    - https://certbot.eff.org/docs/install.html
    - Install `sudo apt-get install python-certbot-nginx` as it's not in certbot-auto manual.
    - `certbot-auto --nginx` and proceed with the wizard.
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
    ```
    git clone https://github.com/fjelltopp/dhis2-dockerisation
    ```
1. \[Optional\] update sql backup files to latest by overwriting `dhis2-dockerisation/country/db-backup.sql`.
1. start it with
    ```
    docker-compose -f docker-compose-country.yml -f docker-compose-ssl.yml up -d
    ```

1. Useful configuration:
    - enable automatic restart on reboot by adding the following to crontab:
         ```
         # at default user crontab, here ubuntu
        @reboot sleep 60 && /usr/local/bin/docker-compose -f /home/ubuntu/dhis2-dockerisation/docker-compose-country.yml up -d

         ```
         The 60 s sleep waits for docker deamon to initialise.
     - automatic ssl cert renewal:
         ```
         # to root crontab
         1 1 * * *  /usr/local/sbin/certbot-auto renew >> /var/log/letsencrypt/certbot_renew.log 2>&1

         ```
        The logs should already by rotated by existing certbot config. But double check the content of the following file:
        ```
        root@puntland-training-hmis:/home/ubuntu# cat /etc/logrotate.d/certbot
        /var/log/letsencrypt/*.log {
            rotate 12
            weekly
            compress
            missingok
        ```

##### Extra:

* It's woth to install psql too:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
