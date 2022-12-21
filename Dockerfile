FROM python:3.10-alpine
COPY . /app
WORKDIR /app
ENV LINK http://www.meetup.com/iabai/
ENV TEXT1 IABAI
ENV TEXT2 IT Solutions
ENV LOGO https://www.iab.ai/assets/iabai_logo_small.png
ENV COMPANY IABAI SaS
RUN curl https://pypi.org/simple/flask/
RUN ls -lah
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt
CMD python rsvp.py
