import pandas as pd
import os
from sqlalchemy import create_engine
import hashlib
from ipaddress import IPv4Address


def md5hash(x: str) -> str:
    """
    Generate an MD5 hash via the hashlib library

    :param x: The string value to which the MD5 hash will be applied
    :return: MD5 hash of parameter 'x'
    """
    return hashlib.md5(x.encode('utf-8')).hexdigest()


MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


if __name__ == "__main__":
    # Create SQLAlchemy engine for Pandas write method
    conn = create_engine(
        f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}",
        # Simple bypass for require_secure_transport=ON in .cnf file; should not be used in the wild
        connect_args={"ssl": {"fake_flag_to_enable_tls": True}}
    )

    # Read file relative to current file directory
    file_path = f"{os.path.dirname(__file__)}/DATASET.xlsx"
    pdf = pd.read_excel(io=file_path, engine="openpyxl")
    # Determine if provided IP address is allocated for public networks
    pdf["is_public_ip"] = pdf["ip_address"].apply(lambda x: IPv4Address(x).is_global)
    # Create new full_name column by concatenating first and last name columns
    pdf["full_name"] = pdf["first_name"] + " " + pdf["last_name"]
    # Create new obfuscated_email column by applying md5 hash to email column
    pdf["obfuscated_email"] = pdf["email"].apply(md5hash)

    pdf.drop(columns=["first_name", "last_name", "email"], inplace=True)

    # Implicitly create table and insert Pandas Dataframe including transformations
    pdf.to_sql(name='data_engineering', con=conn, if_exists='replace', index=False)

    # Kill engine's connection pool
    conn.dispose()
