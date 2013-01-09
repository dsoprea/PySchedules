from xml import sax
from mx import DateTime

from pyschedules.interfaces.ientity_trigger import IEntityTrigger
from pyschedules.interfaces.iprogress_trigger import IProgressTrigger

class XmlCallbacks(sax.ContentHandler, sax.ErrorHandler):
    """SAX content/error handler class for Data Direct XML TV listings"""

    def __init__(self, importer, progress):
        """Create a Data Direct TV listings XML content/error handler"""

        if not issubclass(importer.__class__, IEntityTrigger):
            raise TypeError("Entity-trigger of type [%s] must be an "
                            "IEntityTrigger." % (importer.__class__))

        if not issubclass(progress.__class__, IProgressTrigger):
            raise TypeError("Progress-trigger of type [%s] must be an "
                            "IProgressTrigger." % (progress.__class__))

        self._importer = importer
        self._progress = progress
        self._context = 'root'
        self._contextStack = []
        self._contentList = []
        self._itemTag = None
        self._error = False

        self._statusDict = { 'stations': ('station', 'station'),
                             'lineup': ('map', 'channel mapping'),
                             'schedules': ('schedule', 'schedule'),
                             'programs': ('program', 'program'),
                             'productionCrew': ('member', 'cast/crew member'),
                             'genres': ('genre', 'genre') }

    def _parseDate(self, date):
        if date:
            try:
                return str(DateTime.ISO.ParseDate(date))[:10]
            except Exception, e:
                raise ValueError("Date '%s' is invalid: %s" % (date, e))
        else:
            return None

    def _parseDateTime(self, time):
        if time:
            try:
                return DateTime.ISO.ParseDateTime(time)
            except Exception, e:
                raise ValueError("Time '%s' is invalid: %s" % (time, e))
        else:
            return None

    def _parseDuration(self, duration):
        if duration:
            if duration[0:2] != 'PT' or \
               duration[4] != 'H' or \
               duration[7] != 'M':
                raise ValueError("Duration '%s' is invalid" % duration)
            else:
                try:
                    return int(duration[2:4])*60 + int(duration[5:7])
                except:
                    raise ValueError("Duration '%s' is invalid" % duration)
        else:
            return None

    def _startXTVDNode(self, name, attrs):
        """Process the start of the top-level xtvd node"""

        schemaVersion = attrs.get('schemaVersion')
        validFrom = self._parseDateTime(attrs.get('from'))
        validTo = self._parseDateTime(attrs.get('to'))
        self._progress.printMsg('Parsing version %s data from %s to %s' %
                                    (schemaVersion,
                                     validFrom.strftime('%Y/%m/%d'),
                                     validTo.strftime('%Y/%m/%d')))

    def _startStationsNode(self, name, attrs):
        """Process the start of a node under xtvd/stations"""

        if name == 'station':
            self._stationId = attrs.get('id')
            self._callSign = None
            self._stationName = None
            self._affiliate = None
            self._fccChannelNumber = None

    def _endStationsNode(self, name, content):
        """Process the end of a node under xtvd/stations"""

        if name == 'callSign':
            self._callSign = content
        elif name == 'name':
            self._stationName = content
        elif name == 'affiliate':
            self._affiliate = content
        elif name == 'fccChannelNumber':
            self._fccChannelNumber = content
        elif name == 'station':
            if not self._error:
                self._importer.new_station(self._stationId, self._callSign,
                                          self._stationName, self._affiliate,
                                          self._fccChannelNumber)

    def _startLineupsNode(self, name, attrs):
        """Process the start of a node under xtvd/lineups"""

        if name == 'lineup':
            self._lineupName = attrs.get('name')
            self._location = attrs.get('location')
            self._device = attrs.get('device')
            self._lineupType = attrs.get('type')
            self._postalCode = attrs.get('postalCode')
            self._lineupId = attrs.get('id')
            self._importer.new_lineup(self._lineupName, self._location,
                                     self._device, self._lineupType,
                                     self._postalCode, self._lineupId)

            self._progress.printMsg('Parsing lineup %s' % self._lineupName)
        elif name == 'map':
            self._stationId = attrs.get('station')
            self._channel = attrs.get('channel')
            self._channelMinor = attrs.get('channelMinor')
            self._validFrom = self._parseDateTime(attrs.get('from'))
            self._validTo = self._parseDateTime(attrs.get('to'))
            self._onAirFrom = None
            self._onAirTo = None
        elif name == 'onAir':
            self._onAirFrom = self._parseDateTime(attrs.get('from'))
            self._onAirTo = self._parseDateTime(attrs.get('to'))

    def _endLineupsNode(self, name, content):
        """Process the end of a node under xtvd/lineups"""

        if name == 'map':
            if not self._error:
                self._importer.new_mapping(self._lineupId, self._stationId,
                                          self._channel, self._channelMinor,
                                          self._validFrom, self._validTo,
                                          self._onAirFrom, self._onAirTo)

    def _startSchedulesNode(self, name, attrs):
        """Process the start of a node under xtvd/schedules"""

        if name == 'schedule':
            self._programId = attrs.get('program')
            self._stationId = attrs.get('station')
            self._time = self._parseDateTime(attrs.get('time'))
            self._duration = self._parseDuration(attrs.get('duration'))
            self._new = attrs.has_key('new')
            self._stereo = attrs.has_key('stereo')
            self._subtitled = attrs.has_key('subtitled')
            self._hdtv = attrs.has_key('hdtv')
            self._closeCaptioned = attrs.has_key('closeCaptioned')
            self._ei = attrs.has_key('ei')
            self._tvRating = attrs.get('tvRating')
            self._dolby = attrs.get('dolby')
            self._partNumber = None
            self._partTotal = None
        elif name == 'part':
            self._partNumber = attrs.get('number')
            self._partTotal = attrs.get('total')

    def _endSchedulesNode(self, name, content):
        """Process the end of a node under xtvd/schedules"""

        if name == 'schedule':
            if not self._error:
                self._importer.new_schedule(self._programId, self._stationId,
                                           self._time, self._duration,
                                           self._new, self._stereo,
                                           self._subtitled, self._hdtv,
                                           self._closeCaptioned, self._ei,
                                           self._tvRating, self._dolby,
                                           self._partNumber, self._partTotal)

    def _startProgramsNode(self, name, attrs):
        """Process the start of a node under xtvd/programs"""

        if name == 'program':
            self._programId = attrs.get('id')
            self._series = None
            self._title = None
            self._subtitle = None
            self._description = None
            self._mpaaRating = None
            self._starRating = None
            self._runTime = None
            self._year = None
            self._showType = None
            self._colorCode = None
            self._originalAirDate = None
            self._syndicatedEpisodeNumber = None
            self._advisories = []

    def _endProgramsNode(self, name, content):
        """Process the end of a node under xtvd/programs"""

        if name == 'series':
            self._series = content
        elif name == 'title':
            self._title = content
        elif name == 'subtitle':
            self._subtitle = content
        elif name == 'description':
            self._description = content
        elif name == 'mpaaRating':
            self._mpaaRating = content
        elif name == 'starRating':
            self._starRating = content
        elif name == 'runTime':
            self._runTime = self._parseDuration(content)
        elif name == 'year':
            self._year = content
        elif name == 'showType':
            self._showType = content
        elif name == 'colorCode':
            self._colorCode = content
        elif name == 'originalAirDate':
            self._originalAirDate = self._parseDate(content)
        elif name == 'syndicatedEpisodeNumber':
            self._syndicatedEpisodeNumber = content
        elif name == 'advisory':
            self._advisories.append(content)
        elif name == 'program':
            if not self._error:
                self._importer.new_program(self._programId, self._series,
                                          self._title, self._subtitle,
                                          self._description, self._mpaaRating,
                                          self._starRating, self._runTime,
                                          self._year, self._showType,
                                          self._colorCode,
                                          self._originalAirDate,
                                          self._syndicatedEpisodeNumber,
                                          self._advisories)

    def _startProductionCrewNode(self, name, attrs):
        """Process the start of a node under xtvd/productionCrew"""

        if name == 'crew':
            self._programId = attrs.get('program')
        elif name == 'member':
            self._role = None
            self._givenname = None
            self._surname = None

    def _endProductionCrewNode(self, name, content):
        """Process the end of a node under xtvd/productionCrew"""

        if name == 'role':
            self._role = content
        elif name == 'givenname':
            self._givenname = content
        elif name == 'surname':
            self._surname = content
        elif name == 'member':
            if not self._error:
                if self._givenname:
                    name = '%s %s' % (self._givenname, self._surname)
                else:
                    name = self._surname

                self._importer.new_crew_member(self._programId, self._role,
                                             name, self._givenname, 
                                             self._surname)

    def _startGenresNode(self, name, attrs):
        """Process the start of a node under xtvd/genres"""

        if name == 'programGenre':
            self._programId = attrs.get('program')
        elif name == 'genre':
            self._genre = None
            self._relevance = None

    def _endGenresNode(self, name, content):
        """Process the end of a node under xtvd/genres"""

        if name == 'class':
            self._genre = content
        elif name == 'relevance':
            self._relevance = content
        elif name == 'genre':
            if not self._error:
                self._importer.new_genre(self._programId, self._genre,
                                        self._relevance)

    def startElement(self, name, attrs):
        """Callback run at the start of each XML element"""

        self._contextStack.append(self._context)
        self._contentList = []

        if name in self._statusDict:
            self._itemTag, itemType = self._statusDict[name]
            self._progress.startItem(itemType)
        elif name == self._itemTag:
            self._error = False
            self._progress.newItem()

        try:
            if self._context == 'root':
                if name == 'xtvd':
                    self._context = 'xtvd'
                    self._startXTVDNode(name, attrs)
            elif self._context == 'xtvd':
                self._context = name
            elif self._context == 'stations':
                self._startStationsNode(name, attrs)
            elif self._context == 'lineups':
                self._startLineupsNode(name, attrs)
            elif self._context == 'schedules':
                self._startSchedulesNode(name, attrs)
            elif self._context == 'programs':
                self._startProgramsNode(name, attrs)
            elif self._context == 'productionCrew':
                self._startProductionCrewNode(name, attrs)
            elif self._context == 'genres':
                self._startGenresNode(name, attrs)
        except Exception, e:
            self._error = True
            self._progress.printMsg(str(e), error=True)

    def characters(self, ch):
        """Callback run whenever content is found outside of nodes"""

        self._contentList.append(ch)

    def endElement(self, name):
        """Callback run at the end of each XML element"""

        content = ''.join(self._contentList)

        if name == 'xtvd':
            self._progress.endItems()
        else:
            try:
                if self._context == 'stations':
                    self._endStationsNode(name, content)
                elif self._context == 'lineups':
                    self._endLineupsNode(name, content)
                elif self._context == 'schedules':
                    self._endSchedulesNode(name, content)
                elif self._context == 'programs':
                    self._endProgramsNode(name, content)
                elif self._context == 'productionCrew':
                    self._endProductionCrewNode(name, content)
                elif self._context == 'genres':
                    self._endGenresNode(name, content)
            except Exception, e:
                self._error = True
                self._progress.printMsg(str(e), error=True)

        self._context = self._contextStack.pop()

    def error(self, msg):
        """Callback run when a recoverable parsing error occurs"""

        self._error = True
        self._progress.printMsg('XML parse error: %s' % msg, error=True)

    def fatalError(self, msg):
        """Callback run when a fatal parsing error occurs"""

        self._error = True
        self._progress.printMsg('Fatal XML parse error: %s' % msg, error=True)

    def warning(self, msg):
        """Callback run when a parsing warning occurs"""

        self._progress.printMsg('XML parse warning: %s' % msg)

