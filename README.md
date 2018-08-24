# pytest-testlink
This plugin will set a Testlink controler with a config file (throw a warning if some config error happens) and, after each test, if it have a Test Case in Testlink, it will update its status.

# Configuration
TODO

# Running


## Todo
- [ ] Test the Testlink API
- [ ] Make the plugin:
    - Load config from config file
    - Create new build with test cases of test project
    - Link the tests with the testlink testcases
    - Mark the tests as failed or succeed with custom message
- [ ] Test the plugin:
    - [ ] With connection
    - [ ] Without connection
    - [ ] Bad Configuration File
    - Test Status:
        - [ ] test passed
        - [ ] test failed
        - [ ] test with exception
        - [ ] test skipped
        - [ ] test xfail
        - [ ] test xpassed                                        
- [ ] Create a complete description in the readme