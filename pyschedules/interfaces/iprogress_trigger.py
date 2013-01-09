class IProgressTrigger(object):
    """Triggered throughout processing of data."""

    def printMsg(self, msg, error=False):

        raise NotImplementedError()

    def startItem(self, itemType):

        raise NotImplementedError()

    def newItem(self):

        raise NotImplementedError()

    def endItems(self):

        raise NotImplementedError()

