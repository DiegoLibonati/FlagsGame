from src.constants.defaults import DEFAULT_FLAGS, DEFAULT_MODES


class TestDefaultModes:
    def test_default_modes_is_list(self) -> None:
        assert isinstance(DEFAULT_MODES, list)

    def test_default_modes_is_not_empty(self) -> None:
        assert len(DEFAULT_MODES) > 0

    def test_default_modes_have_required_keys(self) -> None:
        required_keys = ["name", "description", "timeleft", "multiplier"]

        for mode in DEFAULT_MODES:
            for key in required_keys:
                assert (
                    key in mode
                ), f"Mode {mode.get('name', 'unknown')} missing key: {key}"

    def test_default_modes_name_is_string(self) -> None:
        for mode in DEFAULT_MODES:
            assert isinstance(mode["name"], str)

    def test_default_modes_description_is_string(self) -> None:
        for mode in DEFAULT_MODES:
            assert isinstance(mode["description"], str)

    def test_default_modes_timeleft_is_int(self) -> None:
        for mode in DEFAULT_MODES:
            assert isinstance(mode["timeleft"], int)

    def test_default_modes_multiplier_is_int(self) -> None:
        for mode in DEFAULT_MODES:
            assert isinstance(mode["multiplier"], int)

    def test_default_modes_timeleft_is_positive(self) -> None:
        for mode in DEFAULT_MODES:
            assert mode["timeleft"] > 0

    def test_default_modes_multiplier_is_positive(self) -> None:
        for mode in DEFAULT_MODES:
            assert mode["multiplier"] > 0

    def test_default_modes_names_are_unique(self) -> None:
        names = [mode["name"] for mode in DEFAULT_MODES]
        assert len(names) == len(set(names))

    def test_default_modes_contains_normal(self) -> None:
        names = [mode["name"] for mode in DEFAULT_MODES]
        assert "Normal" in names

    def test_default_modes_contains_hard(self) -> None:
        names = [mode["name"] for mode in DEFAULT_MODES]
        assert "Hard" in names

    def test_default_modes_contains_hardcore(self) -> None:
        names = [mode["name"] for mode in DEFAULT_MODES]
        assert "Hardcore" in names


class TestDefaultFlags:
    def test_default_flags_is_list(self) -> None:
        assert isinstance(DEFAULT_FLAGS, list)

    def test_default_flags_is_not_empty(self) -> None:
        assert len(DEFAULT_FLAGS) > 0

    def test_default_flags_have_required_keys(self) -> None:
        required_keys = ["name", "image"]

        for flag in DEFAULT_FLAGS:
            for key in required_keys:
                assert (
                    key in flag
                ), f"Flag {flag.get('name', 'unknown')} missing key: {key}"

    def test_default_flags_name_is_string(self) -> None:
        for flag in DEFAULT_FLAGS:
            assert isinstance(flag["name"], str)

    def test_default_flags_image_is_string(self) -> None:
        for flag in DEFAULT_FLAGS:
            assert isinstance(flag["image"], str)

    def test_default_flags_name_is_not_empty(self) -> None:
        for flag in DEFAULT_FLAGS:
            assert len(flag["name"]) > 0

    def test_default_flags_image_is_url(self) -> None:
        for flag in DEFAULT_FLAGS:
            assert flag["image"].startswith("http")

    def test_default_flags_names_are_unique(self) -> None:
        names = [flag["name"] for flag in DEFAULT_FLAGS]
        assert len(names) == len(set(names))

    def test_default_flags_contains_argentina(self) -> None:
        names = [flag["name"] for flag in DEFAULT_FLAGS]
        assert "Argentina" in names

    def test_default_flags_contains_brasil(self) -> None:
        names = [flag["name"] for flag in DEFAULT_FLAGS]
        assert "Brasil" in names
