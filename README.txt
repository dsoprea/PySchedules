
This is a library built to easily pull down data from Schedules Direct. The 
base implementation of this takes from the xtvd-tools project, but a number of 
major improvements have been made:

> This library simply provides the records from the XML via callbacks, and you
  can do whatever you'd like to do with them (doesn't force you to insert them
  into MySQL tables).
> The "import" object (receives records from the XML) and "progress" object 
  (receives milestone information as various sections of the XML are started 
  and finished) that were in the original implementation are now interfaces to 
  be implemented by the user. Example applications have been provided.
> Some additional "makes sense" parameters have been added to the callbacks for 
  some of the record types.
> I've added the previously-unsupported functionality of downloading 
  channels.conf information from SD (for areas that support it). This requires 
  the line-up ID that you can either get from the XML, or figure out from your 
  account screen on SD's website. This will not include encrypted channels 
  (channels that you may very well have access to, via a CableCard).

Example tools (the first just connects, and presents the various major, 
downloaded sections):

$ python pyschedules/examples/read.py <username> <password>
MSG: Parsing version 1.3 data from 2013/01/09 to 2013/01/10
> Reading section [station].
> Reading section [channel mapping].
MSG: Parsing lineup Comcast West Palm Beach /Palm Beach Co.
> Reading section [schedule].
> Reading section [program].
> Reading section [cast/crew member].
> Reading section [genre].

$ qam FL09567
# Version 1.03 2012-01-26
WBWPLD:561000000:QAM_256:231:73404:586
WTVXDT2:561000000:QAM_256:230:60256:584
WTVXDT4:561000000:QAM_256:225:60892:585
WTVXDT:561000000:QAM_256:435:32728:583
WXELDT2:561000000:QAM_256:201:44124:581
WXELDT3:561000000:QAM_256:203:44126:587
WXELDT4:561000000:QAM_256:202:44128:582
WXELDT:561000000:QAM_256:440:24098:580
WFLXDT:567000000:QAM_256:434:30438:576
WPTVDT2:567000000:QAM_256:216:55949:579
WPTVDT:567000000:QAM_256:432:34580:577
WPBFDT2:573000000:QAM_256:208:56467:554
WPBFDT:573000000:QAM_256:431:31619:551
WPECDT2:573000000:QAM_256:212:32591:553
WPECDT:573000000:QAM_256:433:32590:552

