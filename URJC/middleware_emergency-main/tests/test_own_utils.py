import os
import json
import pytest
from own_utils import load_json

# @pytest.mark.parametrize("preceding_path, file_name, expected_data", [
#     ("test_data", "test_file", {"key": "value"}),
#     ("test_data", "non_existing_file", None),
# ])
# def test_load_json(preceding_path, file_name, expected_data, mocker):
#     # Create a temporary JSON file with test data
#     test_data = {"key": "value"}
#     mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(test_data)))

#     # Call the function under test
#     result = load_json(preceding_path, file_name)

#     # Assert the expected result
#     assert result == test_data

#     # Clean up the temporary file
#     mocker.patch("os.remove")
#     os.remove.assert_called_once_with(f"{preceding_path}/{file_name}.json")


if __name__ == "__main__":
    pytest.main()