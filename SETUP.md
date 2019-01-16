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
    # Default server configuration
    #
    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
            # First attempt to serve request as file, then
            # as directory, then fall back to displaying a 404.
            try_files $uri $uri/ =404;
        }
    }


    server {
        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;
        server_name training.hmissomalia.net www.training.hmissomalia.net; # managed by Certbot


            location / {
            #dhis2 tomcat reverse proxy setup
            proxy_set_header X-Real-IP  $remote_addr;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_set_header Host $host;
            proxy_pass http://127.0.0.1:8080;
            }

        listen [::]:443 ssl ipv6only=on; # managed by Certbot
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/training.hmissomalia.net/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/training.hmissomalia.net/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    }
    server {
        if ($host = training.hmissomalia.net) {
            return 301 https://$host$request_uri;
        } # managed by Certbot
        if ($host = www.training.hmissomalia.net) {
            return 301 https://$host$request_uri;
        } # managed by Certbot


        listen 80 ;
        listen [::]:80 ;
        server_name training.hmissomalia.net www.training.hmissomalia.net;
        return 404; # managed by Certbot


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

## Training instance data synchronisation
Let's configure the training instance to be reset to production data on weekly basis. The setup has two parts; at production server and training server.
### Production
1. Generate rsa keypair \[set `-C` to a meaningful name\]
    ```
    ssh-keygen -t rsa -b 4096 -C "country-production"
    ```
    It's recomended to leave default settings and save private key as default in `~/.ssh/id_rsa`. Also set no passphrase for the key.
1. Upload the public rsa key to the **training** instance `~/.ssh/authorized_keys`
1. Add host named training in `~/.ssh/config` \[set `HostName`\]
    ```
    Host training
    HostName training.instance.hostname.net
    User ubuntu
    ServerAliveInterval 10
    ```
1. Test the connection with
    ```
    ssh training
    ```
1. Make the backup script executable
    ```
    chmod a+x ~/dhis2-dockerisation/util/create_and_send_backup.sh
    ```
1. Add the following entry in crontab
    ```
    10 1 * * 5 /bin/bash -c /home/ubuntu/dhis2-dockerisation/util/create_and_send_backup.sh
    ```
### Training
1. Make the backup restore script executable
    ```
    chmod a+x ~/dhis2-dockerisation/util/receive_db_backup.sh
    ```
1. Add the following entry in crontab. Make sure it happens after the production backup is made and copied. \[set `COUNTRY` accordingly\]
    ```
    30 2 * * 5 COUNTRY=country /bin/bash -c /home/ubuntu/dhis2-dockerisation/util/receive_db_backup.sh
    ```
##### Extra:

* It's woth to install psql too:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
