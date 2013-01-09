#!/usr/bin/python

import sys

from parsedatetime.parsedatetime import Calendar

from pyschedules.interfaces.ientity_trigger import IEntityTrigger
from pyschedules.interfaces.iprogress_trigger import IProgressTrigger

from pyschedules.retrieve import parse_schedules

num_args = len(sys.argv)

if num_args < 3:
    print("Please provide a username and password.")
    sys.exit()

username = sys.argv[1]
password = sys.argv[2]

utc_start = None
utc_stop = None

if num_args >= 5:
    utc_start = Calendar.parse(sys.argv[3])
    utc_stop = Calendar.parse(sys.argv[4])

class EntityTrigger(IEntityTrigger):
    __v_station     = False
    __v_lineup      = False
    __v_mapping     = False
    __v_schedule    = False
    __v_program     = False
    __v_crew_member = False
    __v_genre       = False

    def new_station(self, _id, callSign, name, affiliate, fccChannelNumber):
        """Callback run for each new station"""

        if self.__v_station:
            print("[Station: %s, %s, %s, %s]" % (_id, callSign, name, 
                                                 fccChannelNumber))

    def new_lineup(self, name, location, device, _type, postalCode, _id):
        """Callback run for each new lineup"""

        if self.__v_lineup:
            print("[Lineup: %s, %s, %s, %s, %s, %s]" % 
                  (name, location, device, _type, postalCode, _id))

    def new_mapping(self, lineup, station, channel, channelMinor,
                   validFrom, validTo, onAirFrom, onAirTo):
        """Callback run for each new mapping within a lineup"""

        if self.__v_mapping:
            print("[Mapping: %s, %s, %s, %s, %s, %s, %s, %s]" % 
                  (lineup, station, channel, channelMinor, validFrom, validTo, 
                   onAirFrom, onAirTo))

    def new_schedule(self, program, station, time, duration, new, stereo,
                    subtitled, hdtv, closeCaptioned, ei, tvRating, dolby,
                    partNumber, partTotal):
        """Callback run for each new schedule entry"""

        if self.__v_schedule:
            print("[Schedule: %s, %s, %s, %s, %s]" % (program, station, time, 
                                                      duration, new))

    def new_program(self, _id, series, title, subtitle, description, mpaaRating,
                   starRating, runTime, year, showType, colorCode,
                   originalAirDate, syndicatedEpisodeNumber, advisories):
        """Callback run for each new program entry"""

        if self.__v_program:
            print("[Program: %s, %s, %s, %s, %s, %s, %s, %s, %s]" % 
                  (_id, series, title, subtitle, description, mpaaRating, 
                   starRating, runTime, year))

    def new_crew_member(self, program, role, fullname, givenname, surname):
        """Callback run for each new crew member entry. 'fullname' is a
        derived full-name, based on the presence of 'givenname' and/or 
        'surname'.
        """

        if self.__v_crew_member:
            print("[Crew: %s, %s, %s]" % (program, role, fullname))

    def new_genre(self, program, genre, relevance):
        """Callback run for each new program genre entry"""

        if self.__v_genre:
            print("[Genre: %s, %s, %s]" % (program, genre, relevance))


class ProgressTrigger(IProgressTrigger):
    """Triggered throughout processing of data."""

    items = 0

    def printMsg(self, msg, error=False):

        print("MSG: %s" % (msg))

    def startItem(self, itemType):

        print("> Reading section [%s]." % (itemType))

    def newItem(self):

        pass

    def endItems(self):

        pass

parse_schedules(username, password, EntityTrigger(), ProgressTrigger(), 
                utc_start, utc_stop)

