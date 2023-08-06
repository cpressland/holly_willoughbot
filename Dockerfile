FROM docker.io/python:3.11 as build
WORKDIR /build
ADD . .
RUN pip install poetry
RUN poetry build

FROM docker.io/python:3.11
WORKDIR /app
COPY --from=build /build/dist/*.whl .
RUN pip install *.whl && rm *.whl
COPY --from=build /build/alembic/ ./alembic/
COPY --from=build /build/alembic.ini .

CMD [ "holly", "cron" ]
