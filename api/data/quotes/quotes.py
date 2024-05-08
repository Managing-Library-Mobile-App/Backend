import datetime
import os
import requests

from flask import Response, request
from flask_restful import Resource

from helpers.init import db
from helpers.jwt_auth import verify_jwt_token
from helpers.request_response import create_response
from models import quote_of_the_day, user
from static.responses import (
    TOKEN_INVALID_RESPONSE,
    QUOTES_NOT_WORKING_RESPONSE,
    QUOTES_RESPONSE,
)


class Quotes(Resource):
    def __init__(self) -> None:
        super(Quotes, self).__init__()

    def get(self) -> Response:
        """
        Categories:
        age,alone,amazing,anger,architecture,art,attitude,beauty,best,birthday,business,car,change,communication,
        computers,cool,courage,dad,dating,death,design,dreams,education,environmental,equality,experience,
        failure,faith,family,famous,fear,fitness,food,forgiveness,freedom,friendship,funny,future,
        god,good,government,graduation,great,happiness,health,history,home,hope,humor,imagination,inspirational,
        intelligence,jealousy,knowledge,leadership,learning,legal,life,love,marriage,medical,men, mom, money, morning,
        movies, success
        """
        language: str = request.args.get("language", type=str)
        quotes_api_key = os.environ.get("quotes_api_key")
        category = request.args.get("category", type=str, default="beauty")
        email = verify_jwt_token()
        if not email:
            return create_response(TOKEN_INVALID_RESPONSE, language=language)

        api_url = "https://api.api-ninjas.com/v1/quotes?category={}".format(category)
        response = requests.get(api_url, headers={"X-Api-Key": quotes_api_key})
        if response.status_code != requests.codes.ok:
            return create_response(
                QUOTES_NOT_WORKING_RESPONSE,
                {"details": response.text},
                language=language,
            )

        user_object: user.User = user.User.query.filter_by(email=email).first()

        quote: quote_of_the_day.QuoteOfTheDay = (
            quote_of_the_day.QuoteOfTheDay.query.filter_by(
                user_id=user_object.id
            ).first()
        )
        if (
            not quote
            or datetime.datetime.now().date() - quote.date > datetime.timedelta(days=1)
        ):
            if quote:
                db.session.delete(quote)
                db.session.commit()
            quote = quote_of_the_day.QuoteOfTheDay(
                quote=response.json()[0]["quote"],
                author=response.json()[0]["author"],
                category=response.json()[0]["category"],
                user_id=user_object.id,
            )
            db.session.add(quote)
            db.session.commit()
        return create_response(QUOTES_RESPONSE, quote.as_dict(), language=language)
