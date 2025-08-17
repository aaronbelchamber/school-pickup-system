# School Pickup System - Car Line Automation
Here’s a practical application that can help schools with parent pickup and reduce unpleasant tasks and time burdening school staff.  It really doesn't involve AI in its operational state, but to speed up the development of this prototype I did use some AI to create a free solution.

## This is not a fully built out system but a Proof of Concept!
This would reduce school operational costs and the toil of needing teachers to enter every parent car’s student pick up number manually.  It will also eliminate human errors where people have to stand for almost an hour in all sorts of elements, sometimes in heavy rain or uncomfortable heat to do something we already know we have the technology to automate.

Currently, at my children’s school, there is this unpleasant manual and inefficient process where two teachers have to stand out at the line of cars full of waiting parents and manually enter each number the parents display on a printed card into their cell phone.  This number is sent to a system that alerts the kids waiting that their parents have arrived so they can go to pick up line.

We’re all familiar with QR codes.  These cards should have both a number and a large QR code for a machine to read them.  That will make them at least be “machine ready” when one of the automated solutions is made  available.

Ideally, parents would pull up in line themselves to a scanner mounted to the driver’s side where they could show their card or the QR code on their phone and no teachers would have to stand outside entering in hundreds of numbers every day.  It pains me to see great teacher talent being wasted in such a way.

I do not know if the system the teachers currently use has an open API that would allow input from something other than their cell phones but if the app they are using on their phone doesn’t, it is still possible to have a machine read a number derived from a QR code or the printed digits and enter these numbers as if they were entered into a keyboard.

## System requirements
This is a Python 3.11 project so you need Python installed on your computer.  You need a camera device.  This should work on Windows, Linux or Macs.


## There are two parts to the system: 

1) The app that uses a camera to capture numbers and send the number and 2) a test server to receive responses.
The "test server" just listens to what this app sends and records the number for debugging.  To get this to work in a real world situation, 
this should be a fairly easy step.  Instead of just recording the values into JSON, the server could be built out to take the incoming number, look the number up and cross
reference it against the students linked to it from a simple database table, and display the student numbers in a queue list on a screen.

## Steps to run

1) So you have to activate the virtual environmen (venv). For Windows computers, go to the root of this code and enter:  > `venv/Scripts/activate.bat`

2) If this is the first time running this, packages need to be installed so once you're in the venv, run:
> `python -m pip install -r requirements.txt`

3) Once everything is installed, now let's run the JSON server.  This is to a server that receives the numbers that will get transmitted
from this application and save the data with a timestamp.  This is to show that the tests work, but can easily be built out to send the data
to another system if it has an API to receive these requests.

To run the JSON server, just enter this from the project root:  > `python tests\test_json_server.py`
Keep this terminal window open!  This is where you will see your tests results.

4) Now let's run the app that will open the camera and when it sees digits put in front of it it will read the digits and send them to the JSON server.
Open up another terminal in this root project then enter:  > `python src\car_line_v4.py`

It might take a few seconds to start up before the camera turns on.  

## How to Test
As a test, get a few cards with numbers to show in the camera's view.
Go to the other terminal where you are running the JSON server.
Present your first numeric card in front of the camera, in a few moments, the number should be read and sent to the server.
Did the number show up in the JSON server terminal?

## "car_line" variations
I first created a rough proof of concept for this from scratch in Python but realized there was a lot about the Python libraries that 
were available regarding different ways to prep the camera images and read the digits.

I found the "easyocr" library was simplest to use with the best results.

## Suggest using QR Codes!
QR code reader libraries are very prevalent and much more reliable so I suggest schools print both a human readable number and a QR code 
on the same school pickup card!  At this time, I did not add the QR code reader function but I'll probably get around to that as well.


### Notes
For the above, whenever you see:  > `command here`  only enter the command, do NOT enter the ">" greater than character, that's just what a prompt
usually looks like.  For Mac users, there are a few differences in the paths and how to activate the virtual environment.