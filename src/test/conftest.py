default_test = [("hello", "W2rld")]

#load entry from a file
def file_to_list(file):
    with open(file) as f:
        lines = f.readlines()
    lines = [x.strip("\n") for x in lines]


def pytest_addoption(parser):
    parser.addoption(
        "--stringinput",
        action="append",
        default=default_test,
        help="list of strings inputs to pass to test functions"
    )


def pytest_generate_tests(metafunc):
    if "stringinput" in metafunc.fixturenames:
        metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))