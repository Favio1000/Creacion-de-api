from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


# Create_team
@pytest.mark.parametrize(
    "input_data, missing_field",
    [
        ({"team_name": "Liverpool F.C"}, "city"),     # Caso 1
        ({"city": "Anfield"}, "team_name"),     # Caso 2
    ]
)


def test_create_team_with_missing_fields(customer: TestClient, input_data, missing_field):
    """Test for missing fields, covering both team_name and city"""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    additional_router_team = "/teams/"

    expected_http_code = 422

    customer.post(router_league, json=league)
    response = customer.post(f"{router_league}{league_id}{additional_router_team}", json=input_data)
    
    assert response.status_code == expected_http_code
    assert missing_field in response.json()["detail"][0]["loc"]


def test_create_team_in_test_database(customer):
    """Test for the correct creation of a team"""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    additional_router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}

    expected_http_code = 201
    expected_json = {
        "championship_id": 1,
        "id": 1,
        "team_name": "Liverpool F.C",
        "city": "Anfield"
        }

    customer.post(router_league, json=league)
    response = customer.post(f"{router_league}{league_id}{additional_router_team}", json=team)
    
    assert response.status_code ==expected_http_code
    assert response.json() == expected_json


def test_create_team_with_fewer_than_2_characters(customer):
    """Test for team creation with fewer than 2 characters"""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    additional_router_team = "/teams/"
    team = {"team_name": "L","city": "U"}

    expected_http_code = 422
    min_length = 2

    response = customer.post(router_league, json=league)
    response = customer.post(f"{router_league}{league_id}{additional_router_team}", json=team)

    assert response.status_code == expected_http_code
    assert response.json()["detail"][0]["ctx"]["min_length"] == min_length


def test_create_team_league_does_not_exist(customer):
    """Test for team creation when the associated league does not exist"""

    router_league = "/leagues/"
    league_id = 1
    additional_router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}

    expected_http_code = 404
    expected_json = {
        "detail": "Liga no encontrado para asignarle la equipo."
        }

    response = customer.post(f"{router_league}{league_id}{additional_router_team}", json=team)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_create_team_error_500(customer):
    """Test for creating a team, to verify the HTTP 500 error message."""
 
    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    additional_router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}

    expected_http_code = 500
    expected_json = {"detail":"Fallo en la creacion del equipo en el servidor."}

    customer.post(router_league, json=league)

    with patch("sqlalchemy.orm.Session.commit", side_effect=SQLAlchemyError("Error")):

        response = customer.post(f"{router_league}{league_id}{additional_router_team}", json=team)

        assert response.status_code == expected_http_code
        assert response.json() == expected_json

def test_list_teams_empty(customer):
    """Test the list of teams to verify that it returns an empty list, since no data has been saved yet."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    router_team = "/teams/"

    expected_http_code = 200
    length_list = 0

    customer.post(router_league, json=league)
    response = customer.get(router_team)

    assert response.status_code == expected_http_code
    assert len(response.json()) == length_list


def test_list_teams_containing_one_team(customer):
    """Test for the list of teams, verifying that it returns a list containing a created team."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}

    expected_http_code = 200
    expected_json = {
        "championship_id": 1,
        "id": 1,
        "team_name": "Liverpool F.C",
        "city": "Anfield"
        }

    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)
    response = customer.get(router_team)

    assert response.status_code == expected_http_code
    assert response.json()[0] == expected_json


#Update team
def test_update_team_database(customer):
    """test to verify whether team data is updated."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}
    update_team_id = 1
    update_team = {"team_name": "Manchester United","city": "Old Trafford"}

    expected_http_code = 200
    expected_json = {
            "championship_id": 1,
            "id": 1,
            "team_name": "Manchester United",
            "city": "Old Trafford"
            }


    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)
    response = customer.put(f"{router_team}{update_team_id}", json=update_team)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_update_team_id_not_existe(customer):
    """Team update test verify that the HTTP 404 error is triggered when the ID does not exist."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}
    team_id_not_exist = 2
    update_team = {"team_name": "Manchester United","city": "Old Trafford"}

    expected_http_code = 404
    expected_json = {
            "detail":"Equipo no encontrado para actualizar."
            }


    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)
    response = customer.put(f"{router_team}{team_id_not_exist}", json=update_team)
    
    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_update_team_without_duplicate_names(customer):
    """Team update test to verify that it is not possible to perform an update using the name of an already existing team"""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}
    team_2 = {"team_name": "Manchester United","city": "Old Trafford"}
    update_team_id = 2
    update_team = {"team_name": "Liverpool F.C","city": "Anfield"}

    expected_http_code = 400
    expected_json = {
            "detail":"El nombre del equipo ya está en uso."
            }

    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)
    customer.post(f"{router_league}{league_id}{router_team}", json=team_2)
    response = customer.put(f"{router_team}{update_team_id}", json=update_team)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_update_team_error_500(customer):
    """Test for updating a team, to verify the HTTP 500 error message."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}
    update_team_id = 1
    update_team = {"team_name": "Manchester United","city": "Old Trafford"}

    expected_http_code = 500
    expected_json = {"detail":"Fallo en la actualizacion del servidor"}

    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)


    with patch("sqlalchemy.orm.Session.commit", side_effect=SQLAlchemyError("Error")):

        response = customer.put(f"{router_team}{update_team_id}", json=update_team)

        assert response.status_code == expected_http_code
        assert response.json() == expected_json


def test_delete_team_response(customer):
    """Team delete test to verify if the delete controller is working."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}   
    delete_team_id = 1

    expected_http_code = 200
    expected_json = {"message": f"Equipo con ID {delete_team_id} eliminado correctamente."}


    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)
    response = customer.delete(f"{router_team}{delete_team_id}")

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_delete_team_database(customer):
    """Team delete test to verify that a team can be deleted from the database."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}
    delete_league_id = 1

    expected_http_code = 200
    expected_json = []

    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)
    customer.delete(f"{router_team}{delete_league_id}")
    response = customer.get(router_team)

    assert response.status_code == expected_http_code
    assert response.json() == expected_json

    
def test_delete_team_id_not_existe(customer):
    """Team delete test verify that the HTTP 404 error is triggered when the ID does not exist."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    router_team = "/teams/"
    delete_team_id = 1

    expected_http_code = 404
    expected_json = {
            "detail":"El equipo no existe o ya fue eliminado."
            }
    customer.post(router_league, json=league)
    response = customer.delete(f"{router_team}{delete_team_id}")

    assert response.status_code == expected_http_code
    assert response.json() == expected_json


def test_delete_team_error_500(customer):
    """Test for deleting a team, to verify the HTTP 500 error message."""

    router_league = "/leagues/"
    league = {"league_name": "Premier League","country": "Inglaterra"}
    league_id = 1
    router_team = "/teams/"
    team = {"team_name": "Liverpool F.C","city": "Anfield"}
    delete_league_id = 1

    expected_http_code = 500
    expected_json = {"detail":"Fallo ahora de eliminar en el servidor."}

    customer.post(router_league, json=league)
    customer.post(f"{router_league}{league_id}{router_team}", json=team)


    with patch("sqlalchemy.orm.Session.delete", side_effect=SQLAlchemyError("Error")):

        response = customer.delete(f"{router_team}{delete_league_id}")

        assert response.status_code == expected_http_code
        assert response.json() == expected_json
 
