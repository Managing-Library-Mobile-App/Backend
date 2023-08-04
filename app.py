import datetime

from imports import *

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

from routes import available_routes
from swagger import swagger

if __name__ == "__main__":
    """
    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("Warning log info")
    app.logger.error("Error log info")
    app.logger.critical("Critical log info")
    """
    application_start_date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M")
    logging.basicConfig(
        filename=f"logs/{application_start_date}.log", level=logging.DEBUG
    )
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    app.logger.info("Started the application")
