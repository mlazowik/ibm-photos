FROM python:3-slim AS back

ENV BACK_ROOT /opt/back
RUN mkdir -p $BACK_ROOT
WORKDIR $BACK_ROOT

COPY back/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY back .

#ENV DJANGO_SETTINGS_MODULE="photos.settings"

RUN ./manage.py collectstatic --noinput

FROM node:lts-alpine as front

ENV FRONT_ROOT /opt/front
RUN mkdir -p $FRONT_ROOT
WORKDIR $FRONT_ROOT

COPY front/js/package.json front/js/yarn.lock ./

RUN yarn install

COPY front/js ./

RUN yarn build

FROM nginx:alpine

ENV NGINX_ROOT /opt/nginx
RUN mkdir -p $NGINX_ROOT
WORKDIR $NGINX_ROOT

RUN mkdir static
COPY --from=front /opt/front/build ./
COPY --from=back /opt/back/static static/

COPY front/nginx.conf /etc/nginx/conf.d/photos.template

COPY front/entrypoint.sh /opt/nginx/

RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["sh", "/opt/nginx/entrypoint.sh"]
