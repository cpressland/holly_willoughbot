FROM docker.io/python:3.12 as build
WORKDIR /build
ADD . .
RUN pip install poetry
RUN poetry build

FROM docker.io/python:3.12
WORKDIR /app
COPY --from=build /build/dist/*.whl .
RUN pip install *.whl && rm *.whl

ENV PICCOLO_CONF=holly_willoughbot.piccolo_conf

CMD [ "holly" ]
