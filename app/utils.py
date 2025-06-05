
def assert_corect_api_result(api_result: dict):
    assert api_result
    assert api_result.get('success') is not False
