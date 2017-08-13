# http-monitor
An HTTP Traffic Monitor Command Line Utility


## Problem Statement

*********************************** 
HTTP log monitoring console program 
***********************************

Create a simple console program that monitors HTTP traffic on your machine:

* Consume an actively written-to w3c-formatted HTTP access log (https://en.wikipedia.org/wiki/Common_Log_Format) 
* Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what's before the second '/' in a URL. i.e. the section for "http://my.site.com/pages/create' is "http://my.site.com/pages"), as well as interesting summary statistics on the traffic as a whole. 
* Make sure a user can keep the console app running and monitor traffic on their machine 
* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}” 
* Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered

* Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons. 
* Write a test for the alerting logic 
* Explain how you’d improve on this application design

Please submit here: https://app.greenhouse.io/tests/c56c91edafa7365224a7610e3d9ec22b


## About

This python application monitors HTTP traffic from a Commons Log Format access log. Statistics are gathered about the overall traffic, section counts, and other useful information. Alerts are also generated based off a variable threshold provided as an argument. 

## Installation

The app is built with Python 3.2

`pip install -r requirements.txt`
`./http_monitor.py`

OR Docker

`docker build -t http_monitor .`
`docker run -it http_monitor`

The dockerfile uses an ENTRYPOINT instead of CMD so you can pass args directly to the python script.

`docker run -it http_monitor -t3`

** Make sure to mount any volumes needed if testing a log stream rather than a static file.

## Usage

```
> ./http_monitor.py -h

usage: http_monitor.py [-h] [-a ALERT] [-f FILE] [-w WINDOW]
                       [-t TEST_WINDOW_END] [-t1] [-t2] [-t3]

HTTP Monitor

optional arguments:
  -h, --help            show this help message and exit
  -a ALERT, --alert ALERT
                        Alert threshold (default is 10)
  -f FILE, --file FILE  HTTP Access Log to read from (default reads from
                        requests_at_same_time.log.txt)
  -w WINDOW, --window WINDOW
                        Time window in seconds (default is 120 seconds)
  -t TEST_WINDOW_END, --test_window_end TEST_WINDOW_END
                        Test window upper bound in UTC for testing (ie.
                        "2017-08-08 23:03:20")
  -t1, --test1          Execute Test 1 - uses requests_at_same_time.log.txt
                        which should alert immediately and then resolve
  -t2, --test2          Execute Test 2 - uses apache-fake-log-gen.py to
                        simulate bursty traffic
  -t3, --test3          Execute Test 3 - automated test for alerting logic
```


## Simple Test of Burst Traffic

The http_monitor CLI allows execution of two example runs with options `-t1` and `-t2` and an automated pass/fail test with `-t3`. More information about "test 1", "test 2", and "test 3" are available below.

1. A simple test can be ran using the provided log file `requests_at_same_time.log.txt` with the following CLI parameters:

`./http_monitor.py -t "2017-08-08 23:03:20"`

This will start the time window upper bound at 23:03:20 on August 8th 2017. The log file has 1258 requests to http://google.com/list at 2017-08-08 23:01:27. So the first window will be [23:01:20 to 23:03:20], which will alarm immediately and then exit the window with the burst of requests and recover after about 8 seconds.

2. apache-fake-log-gen.py is included in the root directory. This utility is open source which I modified to test this application. When running the utility, alerts should trigger roughly every 2 minutes and then be resolved.

3. Basically runs test 1 but without the console view and only print a pass/fail. It uses the same `requests_at_same_time.log.txt`, so you can modify that file to make the test fail.

## Design

The application is designed with three main components which all operate in separate threads: Log Watcher, Alerter, and Console. 

The Log Watcher is responsible for polling the log file and parsing out lines into log record objects. I used a library called CLFParser to perform the actual commons log format parsing. When log records are created, they are passed into the Stats service which compiles statistics on the log record. 

The Alerter is simply responsible for checking the Stats service for alerts at a granulatity of 1 second.

The Console is responsible for writing to the screen. I decided to use the curses API to implement the console so that I could predictably update portions of the screen in nice to read tables. 

THere are several helper classes that aid in the organization of the application such as the log_record, log_parser, monitor_args, and the stats data structure  classes. The main entry point is in the http_monitor.py file which only performs setup of threads, the stats data structure, and handles exits cleanly (so you don't get a python exception when CTRL+C'ing).

## Design Improvements

One improvement that would be beneficial is to implement a better Console handler. Curses seemed like a good choice when initially researching for a clean solution, however I had a lot of problems working with the Curses API. There are two paths to a better interface: printing to standard out and clearing the terminal when reprinting the tables or spending more time with the Curses API to implement some of the vast functionality that Curses offers. An example of a pitfall in my application having to do with Curses is the inability to scroll. There is certainly a path to scrolling in Curses (obviously since every Curses app I've ever used has had scroll), but I did not have the time to investigate the solution. 

Another design improvement would be to refactor the Stats data structure. The stats data structure became a catch-all business logic class instead of a pure data structure. A better design would be to charge Stats with adding records to the Stats data structure and another class to handle the querying of Stats for alerts.  

Apart from structure changes, naming could be revised on some of the classes to make clearer of what they do. I like the 3 main thread class names: Console, Alerter, and Log Watcher. Those names give a clear intent for the code inside. Stats is a confusing name and may be better suited as LogRecordRepo if the refactoring of my above improvements were implemented. 

Some further feature improvements that I think would be beneficial would be: database backed alerts and statistics on the traffic, a web interface instead of console interface, and piping log records into a tool like ElasticSearch for search and investigating time windows of traffic.   
