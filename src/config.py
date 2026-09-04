import os
from dotenv import load_dotenv

# Load .env file if exists
load_dotenv()


class Config:
    BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY", "")
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
    ENV = os.getenv("ENV", "development")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    REGISTRY_PATH = os.getenv("REGISTRY_PATH", "registry/registry_v0.json")

    @staticmethod
    def validate():
        missing = []

        if not Config.BASESCAN_API_KEY:
            missing.append("BASESCAN_API_KEY")

        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")


if __name__ == "__main__":
    print("Config loaded:")
    print("BASESCAN_API_KEY:", Config.BASESCAN_API_KEY)
    print("ENV:", Config.ENV)
