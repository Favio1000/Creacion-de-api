# tests/test_league.py
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


# Create_liga
@pytest.mark.parametrize(
    "input_data, missing_field",
    [
        ({"league_name": "La Liga"}, "country"),     # Caso 1
        ({"country": "España"}, "league_name"),     # Caso 2
    ]
)


def test_create_league_with_missing_fields(customer: TestClient, input_data, missing_field):
    """Test for missing fields, covering both league_name and country"""

    router = "/leagues/"

    expected_http_code = 422
    
    response = customer.post(router, json=input_data)
    
    assert response.status_code == expected_http_code
    assert missing_field in response.json()["detail"][0]["loc"]


def test_create_league_in_test_database(customer):
    """Test for the correct creation of a league"""

    router = "/leagues/"
    input_data = {"league_name": "Premier League","country": "Inglaterra"}

    expected_http_code = 201
    expected_json = {
        "id": 1,
        "league_name": "Premier League",
        "country": "Inglaterra"
        }

    response = customer.post(router, json=input_data)
    
    assert response.status_code ==expected_http_code
    assert response.json() == expected_json

    
def test_create_league_with_fewer_than_2_characters(customer):
    """Test for league creation with fewer than 2 characters"""

    router = "/leagues/"
    input_data = {"league_name": "L","country": "U"}

    expected_http_code = 422
    min_length = 2

    response = customer.post(router, json=input_data)

    assert response.status_code == expected_http_code
    assert response.json()["detail"][0]["ctx"]["min_length"] == min_length


def test_create_league_duplicate_name(customer):
    """Test for league creation with duplicate names"""

    router = "/leagues/"
    league = {"league_name": "La Liga","country": "España"}
    duplicate_league = {"league_name": "La Liga","country": "Italia"}

    expected_http_code = 400
    expected_json = {
        "detail": "El nombre de la liga ya está registrado."
        }

    customer.post(router, json=league)
    response = customer.post(router, json=duplicate_league)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json

    
def test_create_league_error_500(customer):
    """Test for creating a league, to verify the HTTP 500 error message."""

    league = {"league_name": "Champions League", "country": "Inglaterra"}
    router = "/leagues/"

    expected_http_code = 500
    expected_json = {"detail":"Fallo en la creacion de liga en el servidor"}


    with patch("sqlalchemy.orm.Session.commit", side_effect=SQLAlchemyError("Error")):

        response = customer.post(router, json=league)

        assert response.status_code == expected_http_code
        assert response.json() == expected_json

#List leagues
def test_list_leagues_empty(customer):
    """Test the list of leagues to verify that it returns an empty list, since no data has been saved yet."""

    router = "/leagues/"

    expected_http_code = 200
    length_list = 0

    response = customer.get(router)

    assert response.status_code == expected_http_code
    assert len(response.json()) == length_list

def test_list_leagues_containing_one_league(customer):
    """Test for the list of leagues, verifying that it returns a list containing a created league"""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}

    expected_http_code = 200
    expected_json = {
            "id": 1,
            "league_name": "Premier League",
            "country": "Inglaterra",
            "teams":[]
            }

    customer.post(router, json=league)
    response = customer.get(router)

    assert response.status_code == expected_http_code
    assert response.json()[0] == expected_json

#Update league
def test_update_league_database(customer):
    """test to verify whether league data is updated."""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    update_league_id = 1
    update_league = {"league_name": "La Liga","country": "España"}

    expected_http_code = 200
    expected_json = {
            "id": 1,
            "league_name": "La Liga",
            "country": "España"
            }


    customer.post(router, json=league)
    response = customer.put(f"{router}{update_league_id}", json=update_league)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_update_league_id_not_existe(customer):
    """League update test verify that the HTTP 404 error is triggered when the ID does not exist."""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id_not_exist = 2
    update_league = {"league_name": "La Liga","country": "España"}

    expected_http_code = 404
    expected_json = {
            "detail":"Liga no encontrada para actualizar."
            }

    customer.post(router, json=league)
    response = customer.put(f"{router}{league_id_not_exist}", json=update_league)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_update_league_without_duplicate_names(customer):
    """League update test to verify that it is not possible to perform an update using the name of an already existing league"""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_2 = {"league_name": "La Liga","country": "España"}
    update_league_id = 1
    update_league = {"league_name": "La Liga","country": "Italia"}

    expected_http_code = 400
    expected_json = {
            "detail":"La liga ya está en uso ."
            }

    customer.post(router, json=league)
    customer.post(router, json=league_2)
    response = customer.put(f"{router}{update_league_id}", json=update_league)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_update_league_error_500(customer):
    """Test for updating a league, to verify the HTTP 500 error message."""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    update_league_id = 1
    update_league = {"league_name": "La Liga","country": "España"}

    expected_http_code = 500
    expected_json = {"detail":"Fallo en la actualizacion del servidor"}

    customer.post(router, json=league)

    with patch("sqlalchemy.orm.Session.commit", side_effect=SQLAlchemyError("Error")):

        response = customer.put(f"{router}{update_league_id}", json=update_league)

        assert response.status_code == expected_http_code
        assert response.json() == expected_json

def test_delete_league_response(customer):
    """League delete test to verify if the delete controller is working."""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    delete_league_id = 1

    expected_http_code = 200
    expected_json = {"message": f"Liga con ID {delete_league_id} eliminado correctamente."}


    customer.post(router, json=league)
    response = customer.delete(f"{router}{delete_league_id}")

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_delete_league_database(customer):
    """League delete test to verify that a league can be deleted from the database."""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    delete_league_id = 1

    expected_http_code = 200
    expected_json = []

    customer.post(router, json=league)
    customer.delete(f"{router}{delete_league_id}")
    response = customer.get(router)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json

def test_delete_league_id_not_existe(customer):
    """League delete test verify that the HTTP 404 error is triggered when the ID does not exist."""

    router = "/leagues/"
    delete_league_id = 1

    expected_http_code = 404
    expected_json = {
            "detail":"La liga no existe o ya fue eliminado."
            }

    response = customer.delete(f"{router}{delete_league_id}")

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_delete_league_error_500(customer):
    """Test for deleting a league, to verify the HTTP 500 error message."""

    router = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    delete_league_id = 1

    expected_http_code = 500
    expected_json = {"detail":"Fallo en la eliminacion del servidor."}

    customer.post(router, json=league)

    with patch("sqlalchemy.orm.Session.delete", side_effect=SQLAlchemyError("Error")):

        response = customer.delete(f"{router}{delete_league_id}")

        assert response.status_code == expected_http_code
        assert response.json() == expected_json
 
