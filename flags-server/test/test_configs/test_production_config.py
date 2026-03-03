from src.configs.default_config import DefaultConfig
from src.configs.development_config import DevelopmentConfig
from src.configs.production_config import ProductionConfig


class TestProductionConfigInheritance:
    def test_inherits_from_default_config(self) -> None:
        assert issubclass(ProductionConfig, DefaultConfig)

    def test_inherits_testing_flag(self) -> None:
        assert ProductionConfig.TESTING is False

    def test_inherits_timezone(self) -> None:
        assert ProductionConfig.TZ == DefaultConfig.TZ

    def test_inherits_mongo_uri(self) -> None:
        assert ProductionConfig.MONGO_URI == DefaultConfig.MONGO_URI

    def test_inherits_mongo_db_name(self) -> None:
        assert ProductionConfig.MONGO_DB_NAME == DefaultConfig.MONGO_DB_NAME

    def test_inherits_mongo_user(self) -> None:
        assert ProductionConfig.MONGO_USER == DefaultConfig.MONGO_USER

    def test_inherits_mongo_pass(self) -> None:
        assert ProductionConfig.MONGO_PASS == DefaultConfig.MONGO_PASS

    def test_inherits_host(self) -> None:
        assert ProductionConfig.HOST == DefaultConfig.HOST

    def test_inherits_port(self) -> None:
        assert ProductionConfig.PORT == DefaultConfig.PORT

    def test_inherits_json_as_ascii(self) -> None:
        assert ProductionConfig.JSON_AS_ASCII == DefaultConfig.JSON_AS_ASCII


class TestProductionConfigOverrides:
    def test_debug_is_false(self) -> None:
        assert ProductionConfig.DEBUG is False

    def test_debug_is_bool(self) -> None:
        assert isinstance(ProductionConfig.DEBUG, bool)

    def test_debug_matches_default(self) -> None:
        assert ProductionConfig.DEBUG == DefaultConfig.DEBUG


class TestProductionConfigEnv:
    def test_env_is_production(self) -> None:
        assert ProductionConfig.ENV == "production"

    def test_env_is_string(self) -> None:
        assert isinstance(ProductionConfig.ENV, str)

    def test_env_not_in_default_config(self) -> None:
        assert not hasattr(DefaultConfig, "ENV")


class TestProductionVsDevelopmentConfig:
    def test_debug_differs_from_development(self) -> None:
        assert ProductionConfig.DEBUG != DevelopmentConfig.DEBUG

    def test_env_differs_from_development(self) -> None:
        assert ProductionConfig.ENV != DevelopmentConfig.ENV
