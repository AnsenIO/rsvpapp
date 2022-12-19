FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
ENV LINK http://www.meetup.com/iabai/
ENV TEXT1 IABAI
ENV TEXT2 IT Solutions
ENV LOGO https://www.iab.ai/assets/iabai_logo_small.png
ENV COMPANY IABAI SaS
RUN pip3 install -r requirements.txt
CMD python rsvp.py
