#STOCK NEWS MONITORING PROJECT

#TODO import modules
import requests
from twilio.rest import Client
import math

#TODO company constants
STOCK = ""
COMPANY_NAME = ""
LIMIT_CHANGE=0.1

#TODO stock_price constants
STOCK_PRICE_API_KEY=""
STOCK_PRICE_PARAMETERS={
"function":"TIME_SERIES_DAILY"
,"symbol":STOCK
,"apikey":STOCK_PRICE_API_KEY
}

#TODO acquire stock price
"""use api call from alphavantage"""

stock_price_response=requests.get(url="https://www.alphavantage.co/query?",params=STOCK_PRICE_PARAMETERS)
print("status_code-",stock_price_response.status_code)
stock_price_json=stock_price_response.json()
date_list=[]
for date in stock_price_json["Time Series (Daily)"]:
    date_list.append(date)
last_close_price=float(stock_price_json["Time Series (Daily)"][date_list[0]]["4. close"].strip())
second_last_close_price=float(stock_price_json["Time Series (Daily)"][date_list[1]]["4. close"].strip())
percentage_change=((last_close_price-second_last_close_price)/last_close_price)*100
print(percentage_change)


#TODO news constants
NEWS_API="856a01ee250d4fbb9ebb892030e1c2e1"
NEWS_PARAMETERS={
    "q":COMPANY_NAME
    ,"from":date_list[18]
    ,"sortBy":"publishedAt"
    ,"apikey":NEWS_API
    ,"language":"en"
}
#TODO acquire news
"""use api call from newsapi.org"""
news_response=requests.get(url="https://newsapi.org/v2/everything?",params=NEWS_PARAMETERS)
print("status_code-",news_response.status_code)
news_json=news_response.json()
print(news_json)
article_list=news_json["articles"]
title_and_news_list=[]
for news in article_list:
    title_and_news_list.append({"title":news["title"],"content":news["content"]})
print(title_and_news_list)

#TODO twilio constants
account_sid="AC1662fc856a3964cb888ed94c8ba83335"
auth_token="7f9907aad9211be811547fa44c65c209"
my_twilio_phno="+19377147194"

#TODO send sms
if percentage_change>LIMIT_CHANGE:
    if percentage_change>0:
        symbol="🔺"
    elif percentage_change<0:
        symbol="🔻"
    print("there is a change")
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"{COMPANY_NAME}:{symbol}{math.ceil(percentage_change)}%\n{50*'-'}\n{title_and_news_list[0]['title']}\n{50*'-'}\n{title_and_news_list[0]['content']}"
             f"\n{50*'-'}\n{title_and_news_list[1]['title']}\n{50*'-'}\n{title_and_news_list[1]['content']}"
             f"\n{50*'-'}\n{title_and_news_list[2]['title']}\n{50*'-'}\n{title_and_news_list[2]['content']}"
        ,from_=my_twilio_phno,
        to="+919633323325"
    )

