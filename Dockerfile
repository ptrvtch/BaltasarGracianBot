FROM python:3.9

# fill in values for tg bot token and ga tracking id
ENV BOT_TOKEN ""
ENV GA_TRACKING_ID "" 


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]