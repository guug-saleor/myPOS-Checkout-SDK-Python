from .Config import Config
from .IPC_Exception import IPC_Exception
from .Defines import Defines
from . import Crypto
import json, base64

class Response():
    __cnf : Config
    __raw_data
    __format
    __data
    __signature

    def __init__(self, cnf:Config, raw_data, format):
        self.__cnf = cnf
        self.__setData(raw_data, format)

    def __setData(self, raw_data, format):
        if not raw_data:
            raise IPC_Exception('Invalid Response data')

        self.__format = format
        self.__raw_data = raw_data

        if self.__format==Defines.COMMUNICATION_FORMAT_JSON:
            self.__data = json.loads(self.__raw_data)
        elif self.__format==Defines.COMMUNICATION_FORMAT_XML:
            self.__data = xmltodict.parse(self.__raw_data)
        elif self.__format==Defines.COMMUNICATION_FORMAT_POST:
            self.__data = self.__raw_data
        else:
            raise IPC_Exception('Invalid response format')

        if not len(self.__data):
            raise IPC_Exception('No IPC Response!')

        self.__extractSignature()

        if (not self.__signature) and self.__data.get('Status') == Defines.STATUS_IPC_ERROR:
            raise IPC_Exception('IPC Response - General Error!')

        self.__verifySignature()
        return self

    def __extractSignature(self):
        self.__signature = self.__data.get('Signature')
        self.__data.pop('Signature', None)
        return True

    def __verifySignature(self):
        if not self.__signature:
            raise IPC_Exception('Missing request signature!')

        if not self.__cnf:
            raise IPC_Exception('Missing config object!')

        if not Crypto.verify(self.__getSignedData(), base64.b64decode(self.__signature), self.__cnf.getAPIPublicKey()):
            raise IPC_Exception('Signature check failed!')

    def __getSignedData(self):
        return base64.b64encode("-".join(str(x) for x in self.__data.values()))

    @classmethod
    def getInstance(cls, cnf:Config, raw_data, format):
        return cls(cnf, raw_data, format)

    def isSignatureCorrect(self):
        try:
            self.__verifySignature()
        except:
            return False

        return True

    def getSignature(self):
        return self.__signature

    def getStatus(self):
        return self.getData('CASE_LOWER').get('status')

    def getData(self, case=None):
        if case==None:
            return self.__data

        if case!='CASE_LOWER':
            return dict((k.lower(), v) for k, v in self.__data.items())
        elif case=='CASE_UPPER':
            return dict((k.upper(), v) for k, v in self.__data.items())
        else:
            raise IPC_Exception('Invalid Key Case!')

    def getStatusMsg(self):
        return self.getData('CASE_LOWER').get('statusmsg')

    def getDataRaw(self):
        return self.__raw_data