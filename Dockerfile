FROM python:3.7 AS builder

RUN pip install --user pipenv

RUN useradd -ms /bin/bash servicex

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

ADD Pipfile.lock Pipfile /home/servicex/

WORKDIR /home/servicex
RUN /root/.local/bin/pipenv sync
RUN /root/.local/bin/pipenv install gunicorn

FROM python:3.7 AS runtime

RUN useradd -ms /bin/bash servicex

COPY --from=builder /home/servicex/.venv /home/servicex/venv

WORKDIR /home/servicex
RUN mkdir ./servicex

COPY README.rst README.rst
COPY setup.py setup.py
COPY setup.cfg setup.cfg
#COPY requirements.txt requirements.txt
#RUN pip install -e .
#RUN pipenv install gunicorn

COPY *.py docker-dev.conf boot.sh ./
COPY servicex/ ./servicex
COPY migrations migrations

RUN chmod +x boot.sh

#ENV FLASK_APP servicex

USER servicex

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
