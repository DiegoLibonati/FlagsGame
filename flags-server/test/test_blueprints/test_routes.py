from flask import Flask
from flask.testing import FlaskClient


class TestBlueprintRegistration:
    def test_flag_blueprint_is_registered(self, app: Flask) -> None:
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert "flag" in blueprint_names

    def test_mode_blueprint_is_registered(self, app: Flask) -> None:
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert "mode" in blueprint_names

    def test_user_blueprint_is_registered(self, app: Flask) -> None:
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert "user" in blueprint_names

    def test_all_blueprints_are_registered(self, app: Flask) -> None:
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert "flag" in blueprint_names
        assert "mode" in blueprint_names
        assert "user" in blueprint_names


class TestFlagRoutesExist:
    def test_flag_alive_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/api/v1/flags/alive" in rule for rule in rules)

    def test_flag_list_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any(rule == "/api/v1/flags/" for rule in rules)

    def test_flag_random_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/random/" in rule and "/api/v1/flags" in rule for rule in rules)

    def test_flag_delete_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/api/v1/flags/<id>" in rule for rule in rules)


class TestModeRoutesExist:
    def test_mode_alive_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/api/v1/modes/alive" in rule for rule in rules)

    def test_mode_list_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any(rule == "/api/v1/modes/" for rule in rules)

    def test_mode_find_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/api/v1/modes/<id>" in rule for rule in rules)

    def test_mode_top_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/top" in rule and "/api/v1/modes" in rule for rule in rules)


class TestUserRoutesExist:
    def test_user_alive_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/api/v1/users/alive" in rule for rule in rules)

    def test_user_top_global_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/top_global" in rule and "/api/v1/users" in rule for rule in rules)

    def test_user_delete_route_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/api/v1/users/<id>" in rule for rule in rules)


class TestRoutesAccessibility:
    def test_flag_alive_is_accessible(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/alive")
        assert response.status_code != 404

    def test_mode_alive_is_accessible(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/alive")
        assert response.status_code != 404

    def test_user_alive_is_accessible(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/alive")
        assert response.status_code != 404

    def test_invalid_route_returns_404(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/nonexistent/")
        assert response.status_code == 404

    def test_wrong_api_version_returns_404(self, client: FlaskClient) -> None:
        response = client.get("/api/v2/flags/alive")
        assert response.status_code == 404


class TestFlagRoutesMethods:
    def test_flags_alive_only_accepts_get(self, client: FlaskClient) -> None:
        response_get = client.get("/api/v1/flags/alive")
        response_post = client.post("/api/v1/flags/alive")
        assert response_get.status_code != 405
        assert response_post.status_code == 405

    def test_flags_list_accepts_get(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/")
        assert response.status_code != 405

    def test_flags_list_accepts_post(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/flags/", json={})
        assert response.status_code != 405

    def test_flags_random_only_accepts_get(self, client: FlaskClient) -> None:
        response_get = client.get("/api/v1/flags/random/5")
        response_post = client.post("/api/v1/flags/random/5")
        assert response_get.status_code != 405
        assert response_post.status_code == 405

    def test_flags_delete_only_accepts_delete(self, client: FlaskClient) -> None:
        fake_id = "507f1f77bcf86cd799439011"
        response_delete = client.delete(f"/api/v1/flags/{fake_id}")
        response_get = client.get(f"/api/v1/flags/{fake_id}")
        assert response_delete.status_code != 405
        assert response_get.status_code == 405


class TestModeRoutesMethods:
    def test_modes_alive_only_accepts_get(self, client: FlaskClient) -> None:
        response_get = client.get("/api/v1/modes/alive")
        response_post = client.post("/api/v1/modes/alive")
        assert response_get.status_code != 405
        assert response_post.status_code == 405

    def test_modes_list_accepts_get(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/")
        assert response.status_code != 405

    def test_modes_list_accepts_post(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/modes/", json={})
        assert response.status_code != 405

    def test_modes_find_only_accepts_get(self, client: FlaskClient) -> None:
        fake_id = "507f1f77bcf86cd799439011"
        response_get = client.get(f"/api/v1/modes/{fake_id}")
        response_post = client.post(f"/api/v1/modes/{fake_id}")
        assert response_get.status_code != 405
        assert response_post.status_code == 405


class TestUserRoutesMethods:
    def test_users_alive_only_accepts_get(self, client: FlaskClient) -> None:
        response_get = client.get("/api/v1/users/alive")
        response_post = client.post("/api/v1/users/alive")
        assert response_get.status_code != 405
        assert response_post.status_code == 405

    def test_users_accepts_post(self, client: FlaskClient) -> None:
        response = client.post(
            "/api/v1/users/",
            json={
                "username": "test",
                "password": "test",
                "mode_id": "507f1f77bcf86cd799439011",
                "score": 0,
            },
        )
        assert response.status_code != 405

    def test_users_accepts_patch(self, client: FlaskClient) -> None:
        response = client.patch(
            "/api/v1/users/",
            json={
                "username": "test",
                "password": "test",
                "mode_id": "507f1f77bcf86cd799439011",
                "score": 0,
            },
        )
        assert response.status_code != 405

    def test_users_delete_only_accepts_delete(self, client: FlaskClient) -> None:
        fake_id = "507f1f77bcf86cd799439011"
        response_delete = client.delete(f"/api/v1/users/{fake_id}")
        response_get = client.get(f"/api/v1/users/{fake_id}")
        assert response_delete.status_code != 405
        assert response_get.status_code == 405

    def test_users_top_global_only_accepts_get(self, client: FlaskClient) -> None:
        response_get = client.get("/api/v1/users/top_global")
        response_post = client.post("/api/v1/users/top_global")
        assert response_get.status_code != 405
        assert response_post.status_code == 405
