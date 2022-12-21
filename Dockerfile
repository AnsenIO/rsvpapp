FROM python
COPY . /app
WORKDIR /app
ENV LINK http://www.meetup.com/iabai/
ENV TEXT1 IABAI
ENV TEXT2 IT Solutions
ENV LOGO https://www.iab.ai/assets/iabai_logo_small.png
ENV COMPANY IABAI SaS
RUN  curl -v https://pypi.org/simple/pip/
RUN ls -lah
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt
CMD python rsvp.py
