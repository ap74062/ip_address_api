from fastapi.testclient import TestClient
from main import app, api_connector, cache_connector, db_connector
import time

test_client = TestClient(app)

db_ping_result_expected = {u'ok': 1.0}


correct_api_call_result_expected = {
    'ip': '134.201.250.155',
    'type': 'ipv4',
    'continent_code': 'NA',
    'continent_name': 'North America',
    'country_code': 'US',
    'country_name': 'United States',
    'region_code': 'CA',
    'region_name': 'California',
    'city': 'Los Angeles',
    'zip': '90013',
    'latitude': 34.04563903808594,
    'longitude': -118.24163818359375,
    'msa': '31100',
    'dma': '803',
    'radius': '0',
    'ip_routing_type': 'fixed',
    'connection_type': 'tx',
    'location': {'geoname_id': 7173700,
                 'capital': 'Washington D.C.',
                 'languages': [{'code': 'en',
                                'name': 'English',
                                'native': 'English'}],
                 'country_flag': 'https://assets.ipstack.com/flags/us.svg',
                 'country_flag_emoji': '🇺🇸',
                 'country_flag_emoji_unicode': 'U+1F1FA U+1F1F8',
                 'calling_code': '1',
                 'is_eu': False}}

incorrect_api_call_result_expected = {
    'success': False,
    'error': {'code': 106,
              'type': 'invalid_ip_address',
              'info': 'The IP Address supplied is invalid.'}}


def test_correct_api_call():
    time.sleep(1)
    api = api_connector()
    time.sleep(1)
    correct_api_call_result_actual = api.get('134.201.250.155')
    assert correct_api_call_result_actual == correct_api_call_result_expected


def test_incorrect_api_call():
    time.sleep(1)
    api = api_connector()
    time.sleep(1)
    incorrect_api_call_result_actual = api.get('test')
    assert incorrect_api_call_result_actual == incorrect_api_call_result_expected


def test_db_connection():
    db = db_connector()
    db_ping_result_actual = db.db.command("ping")
    assert db_ping_result_actual == db_ping_result_expected


def test_cache_connection():
    cache = cache_connector()
    assert cache.client.ping()


def test_db_operations():
    db = db_connector()
    test_db_key = 'test'
    db.collection.delete_many({"ip_address": test_db_key})
    test_db_value = correct_api_call_result_expected

    db.add_row(test_db_key, test_db_value)
    expected_db_test_value = db.get_row(test_db_key)
    assert expected_db_test_value.get('ipstack_result')
    assert expected_db_test_value.get('ipstack_result') == test_db_value

    db.update_row(test_db_key, {'test': True})
    assert db.get_row(test_db_key).get('ipstack_result')
    assert db.get_row(test_db_key).get('ipstack_result') == {'test' : True}

    db.remove_row(test_db_key)
    assert db.get_row(test_db_key) is None

    db.collection.delete_many({"ip_address": test_db_key})


def test_cache_operations():
    cache = cache_connector()
    test_cache_key = 'test'
    test_cache_value = correct_api_call_result_expected

    cache.set(test_cache_key, test_cache_value)
    expected_cache_test_value = cache.get(test_cache_key)
    assert dict(sorted(expected_cache_test_value.items())) == dict(sorted(test_cache_value.items()))

    cache.set(test_cache_key, {})
    assert cache.get(test_cache_key) == {}
