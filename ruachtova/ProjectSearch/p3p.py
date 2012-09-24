P3P_COMPACT = "CP=\"CAO PSA OUR\""  # I import this from a global constants file
# eg. P3P_COMPACT='CP="CAO DSP CURa ADMa DEVa TAIa CONa OUR DELa BUS IND PHY ONL UNI PUR COM NAV DEM STA"'

class MiddlewareResponseInjectP3P(object):
    def __init__(self):
        self.process_response = self.inject

    def inject(self, request, response):
        response['P3P'] = P3P_COMPACT
        return response