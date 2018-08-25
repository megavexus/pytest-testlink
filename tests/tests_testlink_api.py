import pytest
from testlink_sdk import TestlinkApi
from testlink_sdk.exceptions import NoConnectionDataException

@pytest.fixture(scope="class")
def testlink():
    '''Sdk instance with the connection setup'''
    pass


url = "http://localhost/lib/api/xmlrpc/v1/xmlrpc.php"
api_key = "5ab3b3626acf9b83b434f3749a776648"  # TODO:

class TestsTestlinkApiConection(object):
    def test_connection(self):
        testlink_api = TestlinkApi()
        testlink_api.set_host(url)
        testlink_api.set_key(api_key)
        ret = testlink_api.connect()
        assert ret == True


    def test_connection_no_data(self):
        testlink_api = TestlinkApi()
        with pytest.raises(NoConnectionDataException):
            testlink_api.connect()
        

    def test_connection_bad_url(self):
        fake_url = "http://localhost:8000"
        testlink_api = TestlinkApi()
        testlink_api.set_host(fake_url)
        testlink_api.set_key(api_key)
        with pytest.raises(NoConnectionDataException) as e:
            testlink_api.connect()
        exception_msg = e.value.args[0]
        assert 'Not valid Host' in exception_msg

    def test_connection_bad_api_key(self):
        fake_api_key = "AAAA"
        testlink_api = TestlinkApi()
        testlink_api.set_host(url) 
        testlink_api.set_key(fake_api_key)
        with pytest.raises(NoConnectionDataException) as e:
            testlink_api.connect()
        exception_msg = e.value.args[0]
        assert 'Not valid DevKey' in exception_msg


@pytest.fixture(scope="class")
def testlink_sdk():
    testlink_api = TestlinkApi()
    testlink_api.set_host(url)
    testlink_api.set_key(api_key)
    testlink_api.connect()
    return testlink_api

class TestsTestlinkApiProjects(object):
    def test_get_project_plan(self, testlink_sdk):
        project_plan_name = 'Test Project'
        project_plan = testlink_sdk.get_project_plan(project_plan_name)
        assert type(project_plan) == dict
        assert project_plan['prefix'] == "TP"
    
    def test_get_bad_project_plan(self, testlink_sdk):
        project_plan_name = 'ASDFG'
        project_plan = testlink_sdk.get_project_plan(project_plan_name)
        assert project_plan == None

    def test_set_project_plan(self):
        project_plan_name = 'Test Project'
        project_plan = testlink_sdk.set_project_plan(project_plan_name)
        
        pass

    def test_get_build(self):
        pass

    def test_get_not_existent_build(self):
        pass

    def test_set_build(self):
        pass

class TestTestlnik_test_cases(object):
    
    def test_get_test_case(self):
        pass

    def test_get_not_existent_test_case(self):
        pass
    
    def test_set_test_case(self):
        pass

    def test_update_test_case(self):
        pass
