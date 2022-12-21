FROM python:3.8
COPY . /usr/src/app
WORKDIR /usr/src/app
ENV LINK http://www.meetup.com/iabai/
ENV TEXT1 IABAI
ENV TEXT2 IT Solutions
ENV LOGO https://www.iab.ai/assets/iabai_logo_small.png
ENV COMPANY IABAI SaS
RUN which python
RUN python -V
RUN which pip
RUN which pip3
RUN pip3 install -r requirements.txt
CMD python rsvp.py
