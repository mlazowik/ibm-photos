#!/usr/bin/ash

envsubst < /etc/nginx/conf.d/photos.template > /etc/nginx/conf.d/photos.conf

exec nginx -g 'daemon off;'
