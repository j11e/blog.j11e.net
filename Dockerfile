FROM python:3.6-alpine

WORKDIR /blog-j11e

COPY . /blog-j11e

RUN pip install pelican markdown BeautifulSoup4 && \
    rm -rf /var/cache/apk/*

CMD ["pelican", "-s", "/blog-j11e/publishconf.py", "--ignore-cache"]

# build & run with:
# docker build -t blog-j11e .
# docker run --rm -v /path/to/content:/blog-j11e/content -v /path/to/output:/blog-j11e/output blog-j11e
