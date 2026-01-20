FROM python:3.12-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import sys; sys.exit(0)" || exit 1

CMD ["tail", "-f", "/dev/null"]
