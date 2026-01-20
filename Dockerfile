# FROM python:3.12-slim



# WORKDIR /app

# COPY . .

# RUN pip install --no-cache-dir -e .

# CMD ["tail", "-f", "/dev/null"]

FROM python:3.12-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["python", "main.py"]
