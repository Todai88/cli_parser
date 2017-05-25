import argparse

if __name__ == u'__main__':


    """
    Using argparse to parse any passed arguments 
    before sending them to the parser.
    I never worked with argparse before,
    but it seems to be the industry standard.
    """

    parser = argparse.ArgumentParser(
        description=u'CLI parser tool'
    )

    parser.add_argument(
        u'-v',
        dest='verbose',
        default=False,
        help=u'Optional argument to help debugging'
    )

    parser.add_argument(
        u'-t',
        dest='current_time',
        default='16:10',
        help=u'The time from which you wish to check'
    )

    parser.add_argument(
        u'-p',
        dest=u'opt_path',
        default=None,
        help=u'A relative path to a file with newline separated tests'
    )

    parser.add_argument(
        u'-s',
        dest=u'opt_string',
        default=None,
        help=u'A newline ("\n") separated string of cron formatted data'
    )

    arguments = parser.parse_args()

    if(arguments.verbose):
        print(arguments)
