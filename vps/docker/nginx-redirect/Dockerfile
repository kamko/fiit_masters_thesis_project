FROM nginx:1.17.6

WORKDIR /tmp

COPY template.nginx .
COPY entrypoint.sh .

CMD ["bash", "entrypoint.sh"]