# dirwatcher
[![Build Status](https://dev.azure.com/janell-huyck/dirwatcher/_apis/build/status/Janell-Huyck.dirwatcher?branchName=master)](https://dev.azure.com/janell-huyck/dirwatcher/_build/latest?definitionId=1&branchName=master)

This project is a long-running program designed to keep track of what is happening in a specific directory.  Once a second, the program will check the directory for:

    1.  Creation of a file with a specific extension in the watched directory.
    2.  The inclusion in that file of a specific string known as a "magic" string.
    3.  Deletion of a previously watched file from the watched directory

The program will log a message to the terminal once for any of those events.  Files in the monitored directory may be added or deleted or appended at any time by other processes.  It will only scan new text that is added on to the end of text files, rather than watching for changes in the middle of the files.  If the "magic" string is found, it will indicate the file name and the line # that it found the string on.

If the directory to be watched does not exist, it will merely log a notice that it does not exist, and will continue to log that notice every polling interval until the watched directory is created.

When the program starts, it will display a banner indicating it is starting.
When the program finishes, it will display a banner indicating it has finished and the total amount of time that was spent running.  If the program is stopped via SIGTERM or SIGINT, it will exit gracefully, displaying the banner.


## How to run the program:

dirwatcher takes several command-line arguments:

    dir --->    (required) directory to watch
    ext --->    (required) file extension to filter on (example: txt)
    magic ->    (required) the magic text (a string) to watch for
    -poll ->    (optional) integer, in seconds, of how 
                often the program should search.
                This deaults to 1 second.


From your terminal, type in the command:

         $python3 dirwatcher dir ext magic [-pol  seconds]

## Easy way to exit the program:

In the terminal, while the program is running, type in control-C.  That sends a SIGINT to the os, and will interrupt the program, stopping it.
