from testlink-api import TestLinkApi
import configparse
import os

testlink_api = TestLinkApi()


def pytest_addoption(parser):
    """ Turn on testlink features with --testlink option. """
    group = parser.getgroup('testlink')
    group.addoption('--testlik', action="store_true", help="testlik: turn on testlik reporting options")


def pytest_configure(config):
    """ Setup the Testlink class and read the config settings """
    global testlink_api, testlink_setted_up

    config_file_name = "testlink.ini"
    is_test_dir = find_file_in_directories("tests") != None
    
    config_testlink_file = find_file_in_directorioes(config_file_name)
    config_testlink_file_test = find_file_in_directorioes(config_file_name, 'tests')
    
    config_testlink_file = config_testlink_file_test if config_testlink_file_test != None else config_testlink_file

    if config_testlink_file:
        # Coge los datos
        config_tl = configparser.ConfigParser()
        config_tl.read(config_testlink_file)
        if not 'testlink' in config:
            return
        
        api_key = config_tl['testlink']['api-key']
        url = config_tl['testlink']['url']
        testlink_api.set_host()
        testlink_api.set_key()
        testlink_api.connect()

        test_project = config_tl['testlink:project']['test-project-name']
        test_plan = config_tl['testlink:project']['test-plan']
        testlink_api.set_project_plan(test_project)
        testlink_api.set_test_plan(test_plan)

        build = config_tl['testlink:project'].get('build')
        if build:
            testlink_api.set_build(build) # TODO: Crea cuando no exista?

        test_cases = config_tl['testlink:test-cases']
        for test_case_name, test_name in test_cases.items():
            testlink_api.set_relation_test_case_name(test_case_name, test_name)


def pytest_report_header():
    """ Inform of the connection status """
    global testlink_api

    if testlink_api.is_setted_up():
        return "There is no testlink api connection"
    else:
        return "Tests reported to the Testlink in {}, [TestProject: {}, Build:{}]".format(testlink_api.host, testlink_api.test_project, testlink_api.build)


def pytest_report_teststatus(report):
    test_name = report['location'][2]
    test_result = report['outcome']

    global testlink_api

    if testlink_api.is_setted_up():
        testlink_test_case = testlink_api.get_testlink_test_case_from_test_name(test_name)
        testlink_api.update_test_case_execution(testlink_test_case, test_result)
