FROM python:3.8
COPY . /app
WORKDIR /app
ENV LINK http://www.meetup.com/iabai/
ENV TEXT1 IABAI
ENV TEXT2 IT Solutions
ENV LOGO https://www.iab.ai/assets/iabai_logo_small.png
ENV COMPANY IABAI SaS
RUN wget https://pypi.org/simple/pip/
RUN wget https://files.pythonhosted.org/packages/a3/50/c4d2727b99052780aad92c7297465af5fe6eec2dbae490aa9763273ffdc1/pip-22.3.1.tar.gz#sha256=65fd48317359f3af8e593943e6ae1506b66325085ea64b706a998c6e83eeaf38
RUN ls -lah
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt
CMD python rsvp.py
