from flask_restful import reqparse


class RequestParser(reqparse.RequestParser):
    """Custom request parser class."""

    def add_arg(
        self, name: str, type: type = str, required: bool = True, **kwargs
    ) -> None:
        """
        Modified version of add_argument
        :returns: None
        :rtype: None
        """
        self.add_argument(name, type=type, required=required, location="json", **kwargs)
