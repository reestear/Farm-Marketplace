# FROM nginx

# COPY ./default.conf /etc/nginx/conf.d/default.conf
# COPY ./static /var/www/static

FROM caddy:latest

# Copy the Caddyfile to Caddy's configuration directory
COPY ./Caddyfile /etc/caddy/Caddyfile

# Copy the static files to the appropriate directory
COPY ./static /var/www/static
