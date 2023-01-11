## BE-Django-Nw

## With Linux service

```bash
$ sudo nano /etc/systemd/system/sdm.service
```

```bash
[Unit]
Description=%i service with docker compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=/opt/BE-Django-Nw/%i
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d --remove-orphans
ExecStop=/usr/local/bin/docker-compose down --remove-orphans

[Install]
WantedBy=multi-user.target
```