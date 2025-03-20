# import logzero, datetime
# from logzero import logger
# from SmartApi import SmartConnect
# from pyotp import TOTP


# class SmartApiClient:
#     # current date and time
#     now = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")

#     # Initialize the logger
#     logzero.logfile(f"logs/smartapi_client_{now}.log")

#     def __init__(self, api_key: str, api_secret: str, totp_key: str, client_id: str, pin: str):
#         """This class is used to interact with the SmartAPI.

#         Args:
#             api_key (str): API Key from SmartAPI
#             api_secret (str): API Secret from SmartAPI
#             totp_key (str): Secret Key for TOTP authentication
#             client_id (str): Client ID from AngelOne for login
#             pin (str): PIN from AngelOne for login

#         Returns:
#             None
#         """
#         self.api_key = api_key
#         self.api_secret = api_secret
#         self.totp_key = totp_key
#         self.client_id = client_id
#         self.pin = pin
#         self.jwtToken = None
#         self.refreshToken = None
#         self.feedToken = None
#         self.connection = None

#         logger.info("SmartApiClient initialized.")

#     def generate_totp(self):
#         """Generate a TOTP token using the secret key for authentication.

#         Returns:
#             str: TOTP token
#         """
#         try:
#             topt = TOTP(self.totp_key).now()
#         except Exception as e:
#             logger.exception("Exception occurred while generating TOTP: %s", e)
#             raise e
#         else:
#             return topt

#     def generate_session(self):
#         """Generate a session using the SmartConnect.

#         Returns:
#             connection: Connection object for the SmartAPI
#         """
#         try:
#             self.connection = SmartConnect(api_key=self.api_key)
#             totp_token = self.generate_totp()

#             data = self.connection.generateSession(
#                 clientCode=self.client_id,
#                 password=self.pin,
#                 totp=totp_token
#             )

#             if data["status"]:
#                 self.jwtToken = data["data"]["jwtToken"]
#                 self.refreshToken = data["data"]["refreshToken"]
#                 self.feedToken = data["data"]["feedToken"]

#                 logger.info("Session generated successfully to SmartAPI.")

#                 return self.connection
#             else:
#                 logger.error("Session generation failed to SmartAPI: %s", data)
#                 raise Exception("Session generation failed to SmartAPI.")
#         except Exception as e:
#             logger.exception("Exception occurred while generating session to SmartAPI: %s", e)
#             raise e

#     def logout(self):
#         """Logout from SmartAPI session.

#         Returns:
#             None
#         """
#         if self.connection:
#             logger.info("Logging out from SmartAPI.")

#             try:
#                 self.connection.terminateSession(clientCode=self.client_id)
#                 logger.info("Logged out successfully.")
#             except Exception as e:
#                 logger.exception("Exception occurred while logging out: %s", e)
#                 raise e
#             else:
#                 self.connection = None
#                 self.jwtToken = None
#                 self.refreshToken = None
#                 self.feedToken = None
#         else:
#             logger.error("No active session to logout from SmartAPI.")
#             raise Exception("No active session to logout from SmartAPI.")

#     def get_profile(self):
#         """Get the profile details of the user.

#         Returns:
#             dict: Profile details of the user
#         """
#         if not self.refreshToken:
#             logger.error("No active session. Please generate a session first.")
#             raise Exception("No active session. Please generate a session first.")

#         try:
#             profile = self.connection.getProfile(refreshToken=self.refreshToken)
#             logger.info("Profile details fetched successfully.")
#         except Exception as e:
#             logger.exception("Exception occurred while fetching profile details: %s", e)
#             raise e
#         else:
#             return profile


# if __name__ == "__main__":
#     # Example usage of the SmartApiClient
#     import os
#     from dotenv import load_dotenv

#     load_dotenv()

#     API_KEY = os.getenv("API_KEY")
#     API_SECRET = os.getenv("API_SECRET")
#     CLIENT_ID = os.getenv("CLIENT_ID")
#     PIN = os.getenv("PIN")
#     TOTP_KEY = os.getenv("TOTP_KEY")

#     smartapi_client = SmartApiClient(
#         api_key=API_KEY,
#         api_secret=API_SECRET,
#         totp_key=TOTP_KEY,
#         client_id=CLIENT_ID,
#         pin=PIN
#     )

#     connection = smartapi_client.generate_session()
#     profile = smartapi_client.get_profile()
#     # print(profile)
#     smartapi_client.logout()

import logging
import os
import datetime
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
    level=logging.DEBUG,  # Capture all log levels (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=1e6, backupCount=3),  # File logging with rotation
        logging.StreamHandler()  # Console logging
    ]
)

logger = logging.getLogger(__name__)
logger.info("Logging initialized successfully.")


class SmartApiClient:
    def __init__(self, api_key: str, api_secret: str, totp_key: str, client_id: str, pin: str):
        """SmartAPI Client for authentication and session management."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.totp_key = totp_key
        self.client_id = client_id
        self.pin = pin
        self.jwtToken = None
        self.refreshToken = None
        self.feedToken = None
        self.connection = None

        logger.info("SmartApiClient initialized with Client ID: %s", self.client_id)

    def generate_totp(self):
        """Generate a TOTP token using the secret key."""
        try:
            totp = TOTP(self.totp_key).now()
            logger.debug("Generated TOTP token successfully.")
            return totp
        except Exception as e:
            logger.exception("Exception while generating TOTP: %s", e)
            raise

    def generate_session(self):
        """Generate a session using SmartConnect."""
        try:
            logger.info("Attempting to generate session for Client ID: %s", self.client_id)
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

                logger.info("Session generated successfully.")
                return self.connection
            else:
                logger.error("Session generation failed: %s", data)
                raise Exception(f"Session generation failed: {data}")
        except Exception as e:
            logger.exception("Exception while generating session: %s", e)
            raise

    def logout(self):
        """Logout from SmartAPI session."""
        if not self.connection:
            logger.warning("No active session found. Cannot log out.")
            raise Exception("No active session to log out from.")

        logger.info("Logging out from SmartAPI.")

        try:
            response = self.connection.terminateSession(clientCode=self.client_id)
            if response.get("status"):
                logger.info("Logged out successfully.")
            else:
                logger.error("Logout failed: %s", response)
                raise Exception(f"Logout failed: {response}")
        except Exception as e:
            logger.exception("Exception while logging out: %s", e)
            raise
        finally:
            self.connection = None
            self.jwtToken = None
            self.refreshToken = None
            self.feedToken = None
            logger.info("Session cleared after logout.")

    def get_profile(self):
        """Fetch the user's profile details."""
        if not self.connection:
            logger.warning("No active session. Cannot fetch profile.")
            raise Exception("No active session. Please generate a session first.")

        try:
            logger.info("Fetching profile details for Client ID: %s", self.client_id)
            profile = self.connection.getProfile(refreshToken=self.refreshToken)  # Removed refreshToken
            logger.info("Profile details fetched successfully.")
            return profile
        except Exception as e:
            logger.exception("Exception while fetching profile details: %s", e)
            raise


if __name__ == "__main__":
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
        print(profile)  # Print profile for debugging

    finally:
        smartapi_client.logout()
