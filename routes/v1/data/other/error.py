from __future__ import annotations

from datetime import datetime

from flask import jsonify, Response
from flask_restful import Resource, reqparse

import models
from helpers.init import db

from loguru import logger

from models import error


class Error:
    date_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"

    @staticmethod
    def add_entry(level: str, description: str) -> dict[str, str | list]:
        try:
            assert level in [
                "ERROR",
                "INFO",
                "WARNING",
            ], "Valid levels are 'ERROR', 'INFO', 'WARNING'"
            new_error_entry = models.error.Error(
                level=level,
                description=description,
                occurence_date=datetime.strptime(
                    datetime.now().strftime(Error.date_format),
                    Error.date_format,
                ),
            )
            db.session.add(new_error_entry)
            db.session.commit()
            return {"error": new_error_entry.as_dict()}
        except Exception as e:
            exception = "Adding error entry to database failed. {}".format(e)
            logger.error(exception)
            return {"exception": exception}

    @staticmethod
    def delete(start_date_str: str, end_date_str: str) -> dict[str, str | list]:
        try:
            start_date = datetime.strptime(start_date_str, Error.date_format)
            end_date = datetime.strptime(end_date_str, Error.date_format)
            errors = models.error.Error.query.filter(
                models.error.Error.occurence_date.between(start_date, end_date)
            ).all()
            db.session.delete(errors)
            db.session.commit()
            return {"errors": [error_object.as_dict() for error_object in errors]}
        except Exception as e:
            exception = "Deleting errors from database failed. {}".format(e)
            logger.error(exception)
            return {"exception": exception}

    @staticmethod
    def get(
        start_date_str: str | None,
        end_date_str: str | None,
        level: str | None,
    ) -> dict[str, str | list]:
        try:
            if start_date_str is not None and end_date_str is not None:
                if level is not None:
                    start_date = datetime.strptime(start_date_str, Error.date_format)
                    end_date = datetime.strptime(end_date_str, Error.date_format)
                    errors = (
                        models.error.Error.query.filter(
                            models.error.Error.occurence_date.between(
                                start_date, end_date
                            )
                        )
                        .all()
                        .filter_by(level=level)
                        .all()
                    )
                else:
                    start_date = datetime.strptime(start_date_str, Error.date_format)
                    end_date = datetime.strptime(end_date_str, Error.date_format)
                    errors = models.error.Error.query.filter(
                        models.error.Error.occurence_date.between(start_date, end_date)
                    ).all()
            elif start_date_str is None and end_date_str is None:
                if level is not None:
                    errors = models.error.Error.query.filter(
                        models.error.Error.level == level
                    ).all()
                else:
                    errors = models.error.Error.query.all()
            else:
                return {"exception": "Both start date and end date are required"}

            return {"errors": [error_object.as_dict() for error_object in errors]}
        except Exception as e:
            exception = "Getting errors from database failed. {}".format(e)
            logger.error(exception)
            return {"exception": exception}


class ErrorGet(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "level",
            type=str,
            required=False,
            location="json",
        )
        self.reqparse.add_argument(
            "start_date",
            type=str,
            required=False,
            location="json",
        )
        self.reqparse.add_argument(
            "end_date",
            type=str,
            required=False,
            location="json",
        )
        super(ErrorGet, self).__init__()

    def get(self) -> Response:
        args = self.reqparse.parse_args()
        level = args.get("level")
        start_date_str = args.get("start_date")
        end_date_str = args.get("end_date")
        return jsonify(
            Error.get(
                start_date_str=start_date_str, end_date_str=end_date_str, level=level
            )
        )


class ErrorAdd(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "level",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument(
            "description",
            type=str,
            required=True,
            location="json",
        )
        super(ErrorAdd, self).__init__()

    def post(self) -> Response:
        args = self.reqparse.parse_args()
        level = args.get("level")
        description = args.get("description")
        return jsonify(Error.add_entry(level=level, description=description))


class ErrorDelete(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "start_date",
            type=datetime,
            required=True,
            location="json",
        )
        self.reqparse.add_argument(
            "end_date",
            type=datetime,
            required=True,
            location="json",
        )
        super(ErrorDelete, self).__init__()

    def delete(self) -> Response:
        args = self.reqparse.parse_args()
        start_date_str = args.get("start_date")
        end_date_str = args.get("end_date")
        return jsonify(
            Error.delete(start_date_str=start_date_str, end_date_str=end_date_str)
        )


# TODO skrypt zapełniający logi
