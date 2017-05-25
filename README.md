Code challenge provided by Lyst.co.uk for an engineering position (junior).

-----

# Requirements:


Create a tool to help developers / devops to find out when a certain tool will be run next.

Example input might look like:

~~~
30 1 /bin/run_me_daily

45 * /bin/run_me_hourly

* * /bin/run_me_every_minute

* 19 /bin/run_me_sixty_times
~~~
And should give the output:
~~~
1:30 tomorrow - /bin/run_me_daily

16:45 today - /bin/run_me_hourly

16:10 today - /bin/run_me_every_minute

19:00 today - /bin/run_me_sixty_times
~~~


Input was specified to be taken from a file, but in my case I extended it to
also accept strings on the commandline. Just thought that was a fun extension. :)

To initialize the CLI-tool the user needs only to call the package in folder /parser as such:

~~~
python parser -t 16:10 -p tests/basic_tests.txt
~~~

Where -t followed by the time to use for the tests, -p is the path to a file to use.

You can also easily use it using a string (-s) with newline a newline character separating the lines:

~~~
python parser -t 16:10 -s "33 * /bin/run_this \n * 22 /bin/run_this_too"
~~~

----

# Running:

Go to the root of the folder: /cli_parser/ from where you can run the package with python parser <arguments>

<br>

**Arguments**:

-t Time in HH:MM **[required]**

-p Path to a file with operations **[optional]**

-s newline separated string representation of operations **[optional, required when no -p]**

-v Verbose. Work in progress, but helped me during debugging. **[optional]**


See above for some basic examples.

----

I also added some really basics tests in the /tests/ folder. Run them using:
~~~
python -m unittest discover -v
~~~
Not much of a cover, but it's been a long week.