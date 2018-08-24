import pytest

@pytest.fixture(scope="class")
def testlink():
    '''Sdk instance with the connection setup'''
    pass

class TestsTestlinkApi(object):
    def test_connection(self):
        pass

    def test_connection_no_data(self):
        pass

    def test_connection_bad_data(self):
        pass

    def test_get_project(self):
        pass
    
    def test_get_bad_project(self):
        pass

    def test_get_project(self):
        pass

    def test_set_project(self):
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