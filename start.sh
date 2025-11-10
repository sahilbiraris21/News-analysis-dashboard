cd client; npm -i; npm run build
cd ../
# cp ./monitor.conf /etc/nginx/sites-available
# ln -s /etc/nginx/sites-available/monitor.conf /etc/nginx/sites-enabled
# systemctl restart nginx
docker compose up -d 