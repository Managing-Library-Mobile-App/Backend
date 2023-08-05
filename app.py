import datetime

from imports import *
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
api = Api(app)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = 'SECRET_KEY'
toolbar = DebugToolbarExtension(app)

from routes import favicon
from routes import available_routes
from routes import debug_toolbar
from swagger import swagger





if __name__ == "__main__":
    """
    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("Warning log info")
    app.logger.error("Error log info")
    app.logger.critical("Critical log info")
    """
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    application_start_date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M-%S")
    logging.basicConfig(
        filename=f"logs/{application_start_date}.log", level=logging.DEBUG
    )
    app.logger.info("Started the application")
