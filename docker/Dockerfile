ARG PHP_VERSION=8.2
FROM php:${PHP_VERSION}-apache

ARG WWW_UID=1000
ARG WWW_GID=1000

# Sistemske knjižnice in PHP razširitve, ki jih potrebuje WordPress
RUN apt-get update && apt-get install -y --no-install-recommends \
        libfreetype6-dev libjpeg62-turbo-dev libpng-dev libwebp-dev \
        libzip-dev libicu-dev libxml2-dev \
        unzip less default-mysql-client \
    && docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp \
    && docker-php-ext-install -j"$(nproc)" gd mysqli pdo_mysql zip intl exif opcache bcmath \
    && rm -rf /var/lib/apt/lists/*

# Apache: mod_rewrite + AllowOverride All (WordPress permalinki, .htaccess)
RUN a2enmod rewrite headers expires
COPY apache-wp.conf /etc/apache2/conf-available/wp.conf
RUN a2enconf wp

# PHP nastavitve (višji limiti, prikaz napak za razvoj)
COPY php-wp.ini /usr/local/etc/php/conf.d/zz-wp.ini

# WP-CLI
RUN curl -fsSL -o /usr/local/bin/wp \
        https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
    && chmod +x /usr/local/bin/wp

# www-data naj ima UID/GID uporabnika na gostitelju (Linux: brez težav z dovoljenji v ./www)
RUN if [ "$WWW_GID" != "33" ]; then groupmod -o -g "$WWW_GID" www-data; fi \
    && if [ "$WWW_UID" != "33" ]; then usermod -o -u "$WWW_UID" -g "$WWW_GID" www-data; fi

WORKDIR /var/www/html
