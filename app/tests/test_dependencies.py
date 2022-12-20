"""Test cases for methods from dependencies.py."""

import asyncio

import pytest
from fastapi import HTTPException

from app.crud.dependencies import JWTBearer, get_current_user


def test_get_current_user(session, mocker):
    """Test get current user success."""
    mocker.patch("app.crud.utils.get_user_by_username", return_value="string")
    result = asyncio.run(
        get_current_user(
            db=session,
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJpYXQiOjE1MTYyMzkwMjJ9.gKlStbKJNJyTrI-halDo1aRbgMbFaUVoLfb0-HM_bUo",
        )
    )
    assert result == "string"


def test_get_current_user_fails(session):
    """Test get current user fails with user is None and bad token."""
    # user is None
    with pytest.raises(HTTPException):
        asyncio.run(
            get_current_user(
                db=session,
                token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2NzEzNTU0MTF9.NbAAkmEerO_Wm8lNQeLfd_XVIGn-k8-gekVrcgpHUfA",
            )
        )
    # bad token
    with pytest.raises(HTTPException):
        asyncio.run(
            get_current_user(
                db=session,
                token="JleHAiOjE2NzEzNTU0MTF9.NbAAkmEerO_Wm8lNQeLfd_XVIGn-k8-gekVrcgpHUfA",
            )
        )


def test_jwt_bearer():
    """Test verify_token method in JWTBearer class."""
    jwt_bearer = JWTBearer()
    # valid token
    result = jwt_bearer.verify_token(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJpYXQiOjE1MTYyMzkwMjJ9.gKlStbKJNJyTrI-halDo1aRbgMbFaUVoLfb0-HM_bUo"
    )
    assert result
    # wrong token
    result = jwt_bearer.verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ")
    assert not result
    # expired token
    result = jwt_bearer.verify_token(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE2NzE1MzUxNDN9.iSMmHiQhBDrZtkhR07cSuTlLTT5cYFX5jXwgrLfqYIU"
    )
    assert not result
