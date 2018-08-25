import testlink
import logging
from testlink_sdk.exceptions import *

# https://github.com/lczub/TestLink-API-Python-client/blob/master/example/TestLinkExample.py

# TODO: Hablar con vanesa:
    # - Buid: Por cada test usado ,se crea una build? O se selecciona una que ya exista?

class TestlinkApi(object):
    api = None
    api_key = None
    url = None
    test_status = {
        'failed':'f',
        'passed':'p',
        'bloqued':'b',
        # TODO: Completar la lista
    }

    project_plan = None
    test_plan_id = None
    build_id = None
    test_cases = {}

    setted_up = False

    def __init__(self, hostname:str='', key:str=''):
        self.set_host(hostname)
        self.set_key(key)
        self.set_logger()
        
        try:
            self.connect()
        except NoConnectionDataException:
            pass
    
    def set_logger(self):
        self.logger = logging.getLogger("Testlink_Api")
        if not self.logger.hasHandlers():
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)

            logger_format_style = "%(asctime)s (%(name)s) [%(levelname)s]: %(message)s"
            logger_formatter = logging.Formatter(logger_format_style)
            stream_handler.setFormatter(logger_formatter)
            self.logger.addHandler(stream_handler)


    def set_host(self, hostname: str):
        self.hostname = hostname

    def set_key(self, key : str):
        self.api_key = key

    def connect(self):
        if self.hostname == None or self.hostname == '' or self.api_key == None:
            msg = "There are no connection data: hostname and devKey"
            self.logger.error(msg)
            raise NoConnectionDataException(msg)

        self.api = testlink.TestlinkAPIClient(self.hostname, self.api_key)
        try:
            self.about = self.api.about()
            self.setted_up = self.api.checkDevKey()
            self.logger.info("Connection stablished.")
        except testlink.testlinkerrors.TLConnectionError:
            self.setted_up = False
            self.api == None
            msg = "Not valid Hostname. TIP: Is the API path setted? (/lib/api/xmlrpc/v2/xmlrpc.php)"
            self.logger.error(msg)
            raise NoConnectionDataException(msg)
        except testlink.testlinkerrors.TLResponseError:
            self.setted_up = False
            self.api == None
            msg = "Not valid DevKey. Please, contact your Testlink administrator to give you a valid DevKey"
            self.logger.error(msg)
            raise NoConnectionDataException(msg)
        return self.setted_up

    def is_setted_up(self):
        return self.setted_up == True

    ####

    def set_relation_test_case_name(self, testlink_test_case, test_name):
        self.test_cases[test_name] = testlink_test_case

    def get_testlink_test_case_from_test_name(self, test_name):
        return self.test_cases.get(test_name)

    ###

    def get_project_plan(self, project_plan:str):
        try:
            project_plan_data = self.api.getTestProjectByName(project_plan)
            return project_plan_data
        except testlink.testlinkerrors.TLResponseError:
            return None

    def set_project_plan(self, project_plan_name : str):
        data = self.get_project_plan(project_plan_name)
        if data != None:
            self.project_plan = project_plan_name
            self.project_plan_data = data
            self.logger.info("Test Project Plan setted: {} - {}".format(
                self.project_plan_data['prefix'],self.project_plan
            ))
            return self.project_plan
    
    def create_project_plan(self, name:str, description:str=""):
        """ Create a new project plan. TODO: Hacer"""
        pass

    ###    

    def get_build(self, build: str):
        if self.test_plan_id == None:
            raise NoProjectPlanDefinedException

        builds = self.api.getBuildsForTestPlan(self.test_plan_id)
        for build_data in builds:
            if build in build_data['id']:
                self.build_id = build_data['id']
                return self.build_id
            else:
                raise NoBuildFoundException(
                    'Build {} not found n the test plan {} (id={})'.format(self.build, self.test_plan, self.test_plan_id)
                )

    def set_build(self, build : str):        
        try:
            self.build_id = self.get_build(build)
        except NoBuildFoundException:
            self.build_id = self.api.createBuild(self.test_plan_id, build, None)[0]['id']

        self.build = build
        return self.build_id

    ###    
    def get_test_plan(self, test_plan: str):
        if self.test_plan == None:
            raise NoTestPlanDefinedException()

        test_plan_data = self.api.getTestPlanByName(
            self.project_plan, self.test_plan)

    def set_test_plan(self, test_plan : str):
        self.test_plan = test_plan
        self.test_plan_data = self.api.getTestPlanByName( self.project_plan, self.test_plan)[0]
        self.test_plan_id = self.test_plan_data['id']

    ###    

    def get_test_cases(self, status : str = None):
        if status != None and status not in self.test_status:
            raise BadParameterException("There is no test status called '{}'. Statuses permited are: {}".format(status, self.test_status.keys()))

        tests_cases = self.api.getTestCasesForTestPlan(self.test_plan, executestatus=status)
    
    def get_latest_executed_test_case(self, test_case : str):
        test_case_data = self.get_test_case(test_case)
        test_case_id = test_case_data['id']

        latest_test_case_execution = self.get_test_case(test_case_id)[0]
        return latest_test_case_execution

    def get_test_case(self, test_case):
        test_case_data = self.api.getTestCase(None, testcaseexternalid = test_case)[0]
        return test_case_data


    def update_test_case_execution(self, test_case : str, execution_result : str, reason : str = "Automatic execution"):
        if execution_result not in self.test_status:
            raise BadParameterException("There is no test status called '{}'. Statuses permited are: {}".format(status, self.test_status.keys()))

        test_case_data = self.get_test_case(test_case)
        test_case_id = int(test_case_data['id'])-1
        ret = self.api.reportTCResult(
           test_case_id,
           self.test_plan,
           self.build,
           self.test_status[execution_result],
           "" # self.reason
           )

        return ret
