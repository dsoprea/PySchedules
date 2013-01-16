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
    __v_lineup      = True
    __v_mapping     = False
    __v_schedule    = False
    __v_program     = False
    __v_crew_member = False
    __v_genre       = False

    def new_station(self, _id, callSign, name, affiliate, fccChannelNumber):
        """Callback run for each new station"""

        if self.__v_station:
            # [Station: 11440, WFLX, WFLX, Fox Affiliate, 29]
            # [Station: 11836, WSCV, WSCV, TELEMUNDO (HBC) Affiliate, 51]
            # [Station: 11867, TBS, Turner Broadcasting System, Satellite, None]
            # [Station: 11869, WTCE, WTCE, Independent, 21]
            # [Station: 11924, WTVX, WTVX, CW Affiliate, 34]
            # [Station: 11991, WXEL, WXEL, PBS Affiliate, 42]
            # [Station: 12131, TOON, Cartoon Network, Satellite, None]
            # [Station: 12444, ESPN2, ESPN2, Sports Satellite, None]
            # [Station: 12471, WFGC, WFGC, Independent, 61]
            # [Station: 16046, TVNI, TV Chile Internacional, Latin American Satellite, None]
            # [Station: 22233, GOAC020, Government Access - GOAC020, Cablecast, None]
            print("[Station: %s, %s, %s, %s, %s]" % 
                  (_id, callSign, name, affiliate, fccChannelNumber))

    def new_lineup(self, name, location, device, _type, postalCode, _id):
        """Callback run for each new lineup"""

        if self.__v_lineup:
            # [Lineup: Comcast West Palm Beach /Palm Beach Co., West Palm Beach, Digital, CableDigital, 33436, FL09567:X]
            print("[Lineup: %s, %s, %s, %s, %s, %s]" % 
                  (name, location, device, _type, postalCode, _id))

    def new_mapping(self, lineup, station, channel, channelMinor,
                   validFrom, validTo, onAirFrom, onAirTo):
        """Callback run for each new mapping within a lineup"""

        if self.__v_mapping:
            # [Mapping: FL09567:X, 11097, 45, None, 2010-06-29 00:00:00.00, None, None, None]
            print("[Mapping: %s, %s, %s, %s, %s, %s, %s, %s]" % 
                  (lineup, station, channel, channelMinor, validFrom, validTo, 
                   onAirFrom, onAirTo))

    def new_schedule(self, program, station, time, duration, new, stereo,
                    subtitled, hdtv, closeCaptioned, ei, tvRating, dolby,
                    partNumber, partTotal):
        """Callback run for each new schedule entry"""

        if self.__v_schedule:
            # [Schedule: EP012964250031, 70387, 2013-01-16 21:00:00.00, 30, False, True, False, False, True, False, TV-PG, None, None, None]

            print("[Schedule: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                   "%s, %s]" % (program, station, time, duration, new, stereo, 
                   subtitled, hdtv, closeCaptioned, ei, tvRating, dolby, 
                   partNumber, partTotal))

    def new_program(self, _id, series, title, subtitle, description, mpaaRating,
                   starRating, runTime, year, showType, colorCode,
                   originalAirDate, syndicatedEpisodeNumber, advisories):
        """Callback run for each new program entry"""

        if self.__v_program:
            # [Program: EP007501780030, EP00750178, Doctor Who, The Shakespeare Code, Witches cast a spell on the Doctor and Martha., None, None, None, None, Series, None, 2007-04-07, None, []]
            print("[Program: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                  "%s, %s]" % (_id, series, title, subtitle, description, 
                   mpaaRating, starRating, runTime, year, showType, colorCode, 
                   originalAirDate, syndicatedEpisodeNumber, advisories))

    def new_crew_member(self, program, role, fullname, givenname, surname):
        """Callback run for each new crew member entry. 'fullname' is a
        derived full-name, based on the presence of 'givenname' and/or 
        'surname'.
        """

        if self.__v_crew_member:
            # [Crew: EP000036710112, Actor, Estelle Parsons]
            print("[Crew: %s, %s, %s]" % (program, role, fullname))

    def new_genre(self, program, genre, relevance):
        """Callback run for each new program genre entry"""

        if self.__v_genre:
            # [Genre: SP002709210000, Sports event, 0]
            # [Genre: SP002709210000, Basketball, 1]
            # [Genre: SP002737310000, Sports event, 0]
            # [Genre: SP002737310000, Basketball, 1]
            # [Genre: SH016761790000, News, 0]
            # [Genre: SH016761790000, Talk, 1]
            # [Genre: SH016761790000, Interview, 2]
            # [Genre: SH016761790000, Politics, 3]
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

