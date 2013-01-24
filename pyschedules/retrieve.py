import urllib2
import zlib
import logging
import re
import httplib2

from sys import exit
from datetime import datetime, timedelta
from xml import sax

from pyschedules.xml_callbacks import XmlCallbacks

soap_message_xml_template = """<?xml version='1.0' encoding='utf-8'?>
  <SOAP-ENV:Envelope
      xmlns:SOAP-ENV='http://schemas.xmlsoap.org/soap/envelope/'
      xmlns:xsd='http://www.w3.org/2001/XMLSchema'
      xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
      xmlns:SOAP-ENC='http://schemas.xmlsoap.org/soap/encoding/'>
  <SOAP-ENV:Body>
    <tms:download xmlns:tms='urn:TMSWebServices'>
      <startTime xsi:type='tms:dateTime'>%(start_time)s</startTime>
      <endTime xsi:type='tms:dateTime'>%(stop_time)s</endTime>
    </tms:download>
  </SOAP-ENV:Body>
  </SOAP-ENV:Envelope>"""

url = 'http://webservices.schedulesdirect.tmsdatadirect.com/schedulesdirect/tvlistings/xtvdService'
realm = 'TMSWebServiceRealm'

request_headers = { 'Accept-Encoding': 'gzip',
                    'User-Agent':      'pyschedules' }

class GzipStream:
    def __init__(self, fileobj):
        self._fileobj = fileobj
        self._dc = zlib.decompressobj(16+zlib.MAX_WBITS)
        self._buf = ""

    def read(self, size=-1):
        if len(self._buf) == 0:
            self._buf = self._fileobj.read(1024)

        if len(self._buf) > 0:
            result = self._dc.decompress(self._buf, size)
            self._buf = self._dc.unconsumed_tail
        else:
            result = self._dc.flush()

        return result

def get_file_object(username, password, utc_start=None, utc_stop=None):
    """Make the connection. Return a file-like object."""

    if not utc_start:
        utc_start = datetime.now()

    if not utc_stop:
        utc_stop = utc_start + timedelta(1)

    logging.info("Downloading schedules for username [%s] in range [%s] to "
                 "[%s]." % (username, utc_start, utc_stop))

    replacements = { 'start_time': utc_start.strftime('%Y-%m-%dT00:00:00Z'), 
                     'stop_time':  utc_stop.strftime('%Y-%m-%dT00:00:00Z') }

    soap_message_xml = (soap_message_xml_template % replacements)

    authinfo = urllib2.HTTPDigestAuthHandler()
    authinfo.add_password(realm, url, username, password)

    try:
        request = urllib2.Request(url, soap_message_xml, request_headers)
        response = urllib2.build_opener(authinfo).open(request)

        if response.headers['Content-Encoding'] == 'gzip':
            response = GzipStream(response)
    except:
        logging.exception("Could not acquire connection to Schedules Direct.")
        raise

    return response

def process_file_object(file_obj, importer, progress):
    """Parse the data using the connected file-like object."""

    logging.info("Processing schedule data.")

    try:
        handler = XmlCallbacks(importer, progress)
        parser = sax.make_parser()
        parser.setContentHandler(handler)
        parser.setErrorHandler(handler)
        parser.parse(file_obj)
    except:
        logging.exception("Parse failed.")
        raise

    logging.info("Schedule data processed.")

def parse_schedules(username, password, importer, progress, utc_start=None, 
                    utc_stop=None):
    """A utility function to marry the connecting and reading functions."""

    file_obj = get_file_object(username, password, utc_start, utc_stop)
    process_file_object(file_obj, importer, progress)

def get_qam_map(lineup_id):
    
    # The service returns something like "FL09567:X", but its QAM-map service
    # expects something like "FL09567".
    matched = re.match('^[a-zA-Z0-9]+', lineup_id)

    if not matched:
        raise Exception("Lineup ID [%s] is not formatted correctly." % 
                        (lineup_up))

    lineup_id = matched.group(0)
    url = ('https://www.schedulesdirect.org/qam/%s.qam.conf' % (lineup_id))

    h = httplib2.Http()
    resp, content = h.request(url, "GET")

    response_class = int(resp['status'][0])

    if response_class in [4, 5]:
        raise Exception("A QAM-map is not available for lineup-ID [%s]." % 
                        (lineup_id))

    return content

