

def customize_doctest_module():
    from doctest_parser import SageDocTestParser, SageOutputChecker
    import doctest
    doctest.DocTestParser = SageDocTestParser
    doctest.OutputChecker = SageOutputChecker

