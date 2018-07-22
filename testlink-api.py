import testlink

# https://github.com/lczub/TestLink-API-Python-client/blob/master/example/TestLinkExample.py

# TODO: Hablar con vanesa:
    # - Buid: Por cada test usado ,se crea una build? O se selecciona una que ya exista?
class NoConnectionDataException(Exception):
    """ Exception when there are no host or api key at the connection time """

class NoProjectPlanDefinedException(Exception):
    """ Exception given when there is no project plan """

class NoTestPlanDefinedException(Exception):
    """ Exception given when there is no test plan """

class NoBuildFoundException(Exception):
    """ Exception given when there the build is not found """

class BadParameterException(Exception):
    """ Exception thrown when an unnexpected parameter is given """

class TestlinkApi(object):
    api = None
    api_key = None
    url = None
    test_status = {
        'failed':'f',
        # TODO: Completar la lista
    }

    project_plan = None
    test_plan_id = None
    build_id = None


    def __init__(self, host : str, key : str):
        self.set_host(host)
        self.set_key(key)
        self.connect()

    def set_host(self, host : str):
        self.hostname = host

    def set_key(self, key : str):
        self.api_key = key

    def connect(self):
        if self.host == None or self.api_key == None:
            raise NoConnectionDataException()
        
        self.api = testlink.TestlinkAPICliente(self.host, self.api_key)

    def set_project_plan(self, project_plan_name : str):
        self.project_plan = project_plan_name

    def set_build(self, build : str, create_if_no_exist : bool = False):
        if not self.test_plan_id:

        self.build = build
        # TODO: Ver si esto 
        if create_if_no_exist:
            self.build_id = self.api.createBuild(self.test_plan_id, self.build, None)[0]['id']
            return self.build_id
        else:
            builds = self.api.getBuildsForTestPlan(self.test_plan_id)
            for build_data in builds:
                if build in build_data['id']:
                    self.build_id = build_data['id']
                    return self.build_id
            else:
                raise NoBuildFoundException(
                    'Build {} not found n the test plan {} (id={})'.format(self.build, self.test_plan, self.test_plan_id)
                )
            
    def set_test_plan(self, test_plan : str)
        self.test_plan = test_plan
        self.test_plan_data = self.api.getTestPlanByName( self.project_plan, self.test_plan)[0]
        self.test_plan_id = self.test_plan_data['id']


    def get_project_plan(self):
        if self.project_plan == None:
            raise NoProjectPlanDefinedException()

        project_plan_data = self.api.getTestProjectByName(self.project_plan)
        
        return project_plan_data
        
    def get_test_plan(self, test_plan : str):
        if self.test_plan == None:
            raise NoTestPlanDefinedException()

        test_plan_data = self.api.getTestPlanByName(self.project_plan, self.test_plan)

    def get_test_cases(self, status : str = None):
        if status != None and status not in self.test_status:
            raise BadParameterException("There is no test status called '{}'. Statuses permited are: {}".format(status, self.test_status.keys()))

        tests_cases = self.api.getTestCasesForTestPlan(self.test_plan, executestatus=status)
    
    def get_latest_executed_test_case(self, test_case : str):
        test_case_data = self.get_test_case(test_case)
        test_case_id = test_case_data['id']

        latest_test_case_execution = self.getTestCaseByVersion(test_case_id)[0]
        return latest_test_case_execution

    def get_test_case(self, test_case):
        test_case_data = self.api.getTestCase(None, testcaseexternalid = self.test_case)[0]
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
           self.reason)

        return ret


