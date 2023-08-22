import pytest
from db_python_etl.etl import md5hash


# List of tuples containing email value and md5 hash of email value
emails = [
    ("1234567890@example.com", "59556d584ddf28283824ab6e9f1b3076"),
    ("email@example-one.com", "0eb623faabcce12f53374ea7722401e8"),
    ("_______@example.com", "a3230e138a26aa723271acb94ae1386f"),
    ("email@example.name", "2ef659be1fc27bd70f99043e7ad2a27a"),
    ("email@example.museum", "ad3741c78b03ce08bf48c5fe145f5a5d"),
    ("email@example.co.jp", "d772e97dfafc5d66397ad7e5135c09e5")
]


@pytest.mark.parametrize("test_input,expected", emails)
def test_md5hash(test_input, expected):
    assert md5hash(test_input) == expected
