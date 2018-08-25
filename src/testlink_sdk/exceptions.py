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
