# This file contains the SmartApiClient class which is used to interact with the SmartAPI.

import logging, os, datetime
from logging.handlers import RotatingFileHandler
from SmartApi import SmartConnect
from pyotp import TOTP

# Ensure logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Set up log file with rotation
now = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
log_file = f"{log_dir}/smartapi_client_{now}.log"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s : %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=1e6, backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class SmartApiClient:
    def __init__(self, api_key: str, api_secret: str, totp_key: str, client_id: str, pin: str):
        """This class is used to interact with the SmartAPI.

        Args:
            api_key (str): API Key from SmartAPI
            api_secret (str): API Secret from SmartAPI
            totp_key (str): Secret Key for TOTP authentication
            client_id (str): Client ID from AngelOne for login
            pin (str): PIN from AngelOne for login

        Returns:
            None
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.totp_key = totp_key
        self.client_id = client_id
        self.pin = pin
        self.jwtToken = None
        self.refreshToken = None
        self.feedToken = None
        self.connection = None

        logger.info("SmartApiClient initialized.\n")

    def generate_totp(self) -> str:
        """Generate a TOTP token using the secret key for authentication.

        Returns:
            str: TOTP token
        """
        try:
            totp = TOTP(self.totp_key).now()
            logger.debug("TOTP token generated successfully.\n")
            return totp
        except Exception as e:
            logger.exception("Exception occurred while generating TOTP: %s\n", e)
            raise

    def generate_session(self) -> SmartConnect:
        """Generate a session using the SmartConnect.

        Returns:
            SmartConnect: Connection object for the SmartAPI
        """
        try:
            logger.info("Attempting to generate session for Client.\n")
            self.connection = SmartConnect(api_key=self.api_key)
            totp_token = self.generate_totp()

            data = self.connection.generateSession(
                clientCode=self.client_id,
                password=self.pin,
                totp=totp_token
            )

            if data.get("status"):
                self.jwtToken = data["data"]["jwtToken"]
                self.refreshToken = data["data"]["refreshToken"]
                self.feedToken = data["data"]["feedToken"]

                logger.info("Session generated successfully for Client.\n")
                return self.connection
            else:
                logger.error("Session generation failed for Client: %s\n", data)
                raise Exception(f"Session generation failed for Client: {data}\n")
        except Exception as e:
            logger.exception("Exception occurred while generating session for Client: %s\n", e)
            raise

    def logout(self) -> None:
        """Logout from SmartAPI session for Client.

        Returns:
            None
        """
        if not self.connection:
            logger.warning("No active session found. Cannot logout.\n")
            raise Exception("No active session to logout from.\n")

        logger.info("Logging out from SmartAPI.\n")

        try:
            response = self.connection.terminateSession(clientCode=self.client_id)
            if response.get("status"):
                logger.info("Logged out successfully.\n")
            else:
                logger.error("Logout failed: %s\n", response)
                raise Exception(f"Logout failed: {response}\n")
        except Exception as e:
            logger.exception("Exception occurred while logging out: %s\n", e)
            raise
        finally:
            self.connection = None
            self.jwtToken = None
            self.refreshToken = None
            self.feedToken = None

    def get_profile(self):
        """Fetch the profile details for Client.

        Returns:
            dict: Profile details of the Client.
        """
        if not self.connection:
            logger.warning("No active session. Please generate a session first.\n")
            raise Exception("No active session. Please generate a session first.\n")

        try:
            logger.info("Fetching profile details for Client.\n")
            profile = self.connection.getProfile(refreshToken=self.refreshToken)
            logger.info("Profile details fetched successfully.\n")
            return profile
        except Exception as e:
            logger.exception("Exception occurred while fetching profile details: %s\n", e)
            raise


if __name__ == "__main__":
    # Example usage of the SmartApiClient
    from dotenv import load_dotenv

    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    CLIENT_ID = os.getenv("CLIENT_ID")
    PIN = os.getenv("PIN")
    TOTP_KEY = os.getenv("TOTP_KEY")

    try:
        smartapi_client = SmartApiClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            totp_key=TOTP_KEY,
            client_id=CLIENT_ID,
            pin=PIN
        )

        connection = smartapi_client.generate_session()
        profile = smartapi_client.get_profile()
        print(profile)
    finally:
        smartapi_client.logout()
