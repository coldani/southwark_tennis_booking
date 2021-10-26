# Book tennis courts in London

This program tries to book a tennis court slot in either Southwark Park or Tanner Street Park in Southwark, London.

It has one main file, `book_tennis_court.py`, which uses functions from `helper.py` and data from `constants.py`. 

`book_tennis_court.py` can be run directly from the command line by invoking the python interpreter. It takes 3 argument:
* `times` (positional arguments): indicate when (at what time) we want to book the court for
  * must be expressed in the form `hour:minute` (e.g. `8:00`)
  * can be as many as you like (in case we have more than one option that works for us and we want to maximise the probability of finding an available court)
* `--date` (or `-d`): the day we want to book the court for
  * can be expressed in absolute terms (in the form `yyyy-mm-dd`) or in relative terms (from `0` to `7`), in which case it would indicate the day falling `x`days in the future
  * accepts only 1 value
* `--wait` (or `-w`): used to let the script know if we want to run it immediately or stop execution until a given time
  * can be `no` (if we want to run the entire script immediately) or in the form `hour:minute:second` (e.g. `20:0:0` (8pm))
  * accepts only 1 value

## Usage
`python book_tennis_court.py [-h] [--date [DATE]] [--wait [WAIT]] [times]`

A help message can be displayed by typing: `python book_tennis_court.py -h`, which results in the message below appearing to the screen:
```
positional arguments:
times:  {8:00,8:30,9:00,9:30,10:00,10:30,11:00,11:30,12:00,12:30,13:00,13:30,14:00,
14:30,15:00,15:30,16:00,16:30,17:00,17:30,18:00,18:30,19:00,19:30,20:00,20:30}
                        The times that the script will try to book

optional arguments:
  -h, --help    show this help message and exit
  --date [DATE], -d [DATE]
                        The date that the script will try to book. Can be a
                        date, in which case it needs to be in the form 'yyyy-
                        mm-dd', or an integer, in which case it will indicate
                        the day falling 'date' days in the future.
                        Defaults to 7 (i.e. the day falling one week in the future)
  --wait [WAIT], -w [WAIT]
                        The time that the script will wait until making the
                        booking. Can either be 'no' (if we want to book
                        immediately) or be expressed in 'hour:minute:second').
                        Defaults to '20:0:0' (8pm)
```

### Some examples

#### Basic example
The booking system opens at 8pm each day for the day falling one week in the future. 
So, assuming we are on a Saturday (before 8pm!), the following command will make the script to book a slot at 4.00pm for the following Saturday:

`python book_tennis_court.py 16:00`

This is because the default values for `--date` and `--wait` are `7` (i.e., 7 days in the future) and `20:0:0` (i.e., 8pm) respectively.

#### Second example
Let's now assume we are on a Friday and would like to play the next day, but all courts have been booked.
The only thing we can do is to hope that someone cancels their booking and book it ourselves - however free slots usually disappear really soon, so we need to keep checking and checking and checking!

We can authomate this by having our script run every, say, 5 minutes, which will check if a booking has been cancelled, in which case it will book it for us! 
Assuming we are free to play anytime between 9am and 11.30am (i.e. the last full hour would be from 10:30 to 11:30), the correct command would be:

`python book_tennis_court.py 9:00 9:30 10:00 10:30 -w no -d 1`

We can then make it run every 5 minutes with, for example, the cron utility (on Linux and MacOS) and hope that someone indeed cancel their booking :).

If we want to keep our script running overnight (so that past midnight it will need to try and book for the same day, not the day after), we should specify the date 
as follows (let's assume today is 26th October 2021):

`python book_tennis_court.py 9:00 9:30 10:00 10:30 -w no -d 2021-10-27`


