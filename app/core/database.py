import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from google.cloud.sql.connector import Connector, IPTypes

load_dotenv()

def init_engine():
    db_provider = os.getenv("DB_PROVIDER", "SUPABASE").upper()

    if db_provider == "GCP":
        print("🔗 Connecting to GCP Cloud SQL...")
        connector = Connector()

def init_engine():
    db_provider = os.getenv("DB_PROVIDER", "SUPABASE").upper()

    if db_provider == "GCP":
        print("🔗 Connecting to GCP Cloud SQL...")
        connector = Connector()

        def getconn():
            # GCP-specific IP and IAM logic
            ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") == "True" else IPTypes.PUBLIC
            user, enable_iam_auth = (
                (os.getenv("DB_IAM_USER"), True)
                if os.getenv("DB_IAM_USER")
                else (os.getenv("DB_USER"), False)
            )
            
            return connector.connect(
                os.getenv("INSTANCE_CONNECTION_NAME"),
                "pg8000",
                user=user,
                password=os.getenv("DB_PASS", ""),
                db=os.getenv("DB_NAME"),
                ip_type=ip_type,
                enable_iam_auth=enable_iam_auth,
            )

        # GCP uses pg8000 driver via the 'creator' function
        return create_engine("postgresql+pg8000://", creator=getconn)

    elif db_provider == "SUPABASE":
        print("🔗 Connecting to Supabase...")
        db_url = os.getenv("SUPABASE_DB_URL")
        if not db_url:
            raise ValueError("SUPABASE_DB_URL environment variable not set.")
        
        # Use NullPool for Supabase serverless/lambda functions to avoid connection leaks
        # For long-running servers, you can remove poolclass=NullPool
        # Defaulting to serverless-safe NullPool if not specified otherwise.
        return create_engine(
            db_url, 
            poolclass=NullPool if os.getenv("IS_SERVERLESS") != "False" else None
        )

    else:
        raise ValueError(f"Unknown DB_PROVIDER: {db_provider}")

# Initialize
engine = init_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
