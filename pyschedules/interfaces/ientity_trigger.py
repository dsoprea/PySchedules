class IEntityTrigger(object):
    def new_station(self, _id, callSign, name, affiliate, fccChannelNumber):
        """Callback run for each new station"""

        raise NotImplementedError()

    def new_lineup(self, name, location, device, _type, postalCode, _id):
        """Callback run for each new lineup"""

        raise NotImplementedError()

    def new_mapping(self, lineup, station, channel, channelMinor,
                   validFrom, validTo, onAirFrom, onAirTo):
        """Callback run for each new mapping within a lineup"""

        raise NotImplementedError()

    def new_schedule(self, program, station, time, duration, new, stereo,
                    subtitled, hdtv, closeCaptioned, ei, tvRating, dolby,
                    partNumber, partTotal):
        """Callback run for each new schedule entry"""

        raise NotImplementedError()

    def new_program(self, _id, series, title, subtitle, description, mpaaRating,
                   starRating, runTime, year, showType, colorCode,
                   originalAirDate, syndicatedEpisodeNumber, advisories):
        """Callback run for each new program entry"""

        raise NotImplementedError()

    def new_crew_member(self, program, role, fullname, givenname, surname):
        """Callback run for each new crew member entry. 'fullname' is a
        derived full-name, based on the presence of 'givenname' and/or 
        'surname'.
        """

        raise NotImplementedError()

    def new_genre(self, program, genre, relevance):
        """Callback run for each new program genre entry"""

        raise NotImplementedError()

