FROM python:3.10

WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY Pipfile* ./
RUN pip install pipenv && pipenv install
COPY . .

CMD [ "python", "./main.py" ]