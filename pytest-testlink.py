from testlink-api import TestLinkApi

testlink_api = TestLinkApi(None, None)
# TODO: Setup del test

def putest_addoption(parser):
    """ Turn on testlink features with --testlink option. """
    group = parser.getgroup('testlink')
    group.addoption('--testlik', action="store_true", help="testlik: turn on testlik reporting options")

def pytest_report_header():
    """ Inform of the connection status """
    global testlink_api

    if testlink_api.api != None:
        return "There is no testlink api connection"
    else:
        return "Tests reported to the Testlink in {}, [TestProject: {}, Build:{}]".format(testlink_api.host, testlink_api.test_project, testlink_api.build)

def pytest_report_teststatus(report):
    test_name = report.name
    # TODO: Si existe::
        # 1. Obtiene si hay un test relacionado
        # 2. Obtiene el estado de la anterior ejecución
        # 3. Reporta el estado anterior y el nuevo.
        # 4. Actualiza el estado del test.
