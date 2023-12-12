from datetime import datetime

from flask_restful import Resource, reqparse

from helpers.init import cursor, conn

from loguru import logger


class Error:
    @staticmethod
    def get_all() -> list:
        try:
            cursor.execute(""" SELECT * FROM error""")
            all_errors = cursor.fetchall()
            print(all_errors)
            return all_errors
        except Exception as e:
            logger.error("Adding error entry to database failed. %s", e)
            return []

    @staticmethod
    def get_last_n(rows_count: int = 100) -> list:
        try:
            cursor.execute(""" SELECT * FROM error LIMIT %s""", (rows_count,))
            last_n_errors = cursor.fetchall()
            print(last_n_errors)
            return last_n_errors
        except Exception as e:
            logger.error("Adding error entry to database failed. %s", e)
            return []

    @staticmethod
    def get_by_date(date: datetime) -> list:
        try:
            day_start = datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=0,
                minute=0,
                second=0,
            )
            day_end = datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=23,
                minute=59,
                second=59,
            )
            cursor.execute(
                """ SELECT * FROM error WHERE occurence_date BETWEEN %s AND %s""",
                (
                    day_start,
                    day_end,
                ),
            )
            all_errors_from_one_day = cursor.fetchall()
            print(all_errors_from_one_day)
            return all_errors_from_one_day
        except Exception as e:
            logger.error("Adding error entry to database failed. %s", e)
            return []

    @staticmethod
    def add_entry(message: str, details: str) -> bool:
        try:
            cursor.execute(
                """INSERT INTO error (occurence_date, type, description) 
                VALUES (%s, %s, %s)""",
                (
                    datetime.now(),
                    message,
                    details,
                ),
            )
            conn.commit()
            print("added entry")
            return True
        except Exception as e:
            logger.error("Adding error entry to database failed. %s", e)
            return False


class ErrorGetAll(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        super(ErrorGetAll, self).__init__()

    def get(self) -> dict[str, list]:
        errors_all = Error.get_all()
        return {"errors": errors_all}


class ErrorGetLastN(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "rows_count",
            type=int,
            required=False,
            location="json",
        )
        super(ErrorGetLastN, self).__init__()

    def get(self) -> dict[str, list]:
        args = self.reqparse.parse_args()
        rows_count = args.get("rows_count")
        if rows_count is not None:
            errors_all = Error.get_last_n(rows_count)
        else:
            print("no rows_count specified")
            errors_all = Error.get_last_n()
        return {"errors": errors_all}


class ErrorGetByDate(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "date",
            type=datetime,
            required=True,
            location="json",
        )
        super(ErrorGetByDate, self).__init__()

    def get(self) -> dict[str, list]:
        args = self.reqparse.parse_args()
        date = args.get("date")


class ErrorAddEntry(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "message",
            type=str,
            required=True,
            location="json",
        )
        self.reqparse.add_argument(
            "details",
            type=str,
            required=True,
            location="json",
        )
        super(ErrorAddEntry, self).__init__()

    def post(self) -> dict[str, list]:
        args = self.reqparse.parse_args()
        message = args.get("message")
        details = args.get("details")


errorek = Error()
errorek.get_all()
errorek.add_entry(message="index error", details="very bad")
errorek.get_all()
errorek.get_by_date(date=datetime.now())
errorek.add_entry(message="index error 2", details="very very bad")
errorek.get_last_n()
