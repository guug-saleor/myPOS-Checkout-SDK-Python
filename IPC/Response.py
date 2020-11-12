import base64
import json
from typing import Dict

import xmltodict

from IPC import Crypto
from IPC.Defines import Defines
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class Response(object):
    """
 * IPC Response class. Parse and validate income __data
    """
    __cnf: Config
    __raw_data = None
    __format = None
    __data: Dict[str, str]
    __signature: str

    def __init__(self, cnf: Config, raw_data, format):
        """\n
    * @param cnf: Config
    * @param string|array raw_data
    * @param string format COMMUNICATION_FORMAT_JSON|COMMUNICATION_FORMAT_XML|COMMUNICATION_FORMAT_POST\n
    * @raises IPC_Exception
        """
        self.__cnf = cnf
        self.__setData(raw_data, format)

    def __setData(self, raw_data, format):
        """
    * @param raw_data
    * @param format\n
    * @return self
    * @raises IPC_Exception
        """
        if not bool(raw_data):
            raise IPC_Exception('Invalid Response data')

        self.__format = format
        self.__raw_data = raw_data

        if format == Defines.COMMUNICATION_FORMAT_JSON:
            self.__data = Dict[str, str](json.loads(self.__raw_data))
        elif format == Defines.COMMUNICATION_FORMAT_XML:
            self.__data = xmltodict.parse(self.__raw_data)
            if self.__data['@attributes']:
                del self.__data['@attributes']
        elif format == Defines.COMMUNICATION_FORMAT_POST:
            self.__data = self.__raw_data
        else:
            raise IPC_Exception('Invalid response format!')

        if not bool(self.__data):
            raise IPC_Exception('No IPC Response!')

        self.__extractSignature()

        if not bool(self.__signature) and ('Status' in self.__data) and self.__data['Status'] == Defines.STATUS_IPC_ERROR:
            raise IPC_Exception('IPC Response - General Error!')

        self.__verifySignature()

        return self

    def __extractSignature(self):
        # TODO: select one of (list, dict)
        if bool(self.__data) and isinstance(self.__data, (list, dict)):
            for k, v in self.__data:
                if k.lower() == '__signature':
                    self.__signature = v
                    del self.__data[k]

        return True

    def __verifySignature(self):
        """
    * @raises IPC_Exception
        """
        if not bool(self.__signature):
            raise IPC_Exception('Missing request __signature!')

        if not self.__cnf:
            raise IPC_Exception('Missing config object!')

        pubKey = self.__cnf.getAPIPublicKey()
        if not Crypto.verify(self.__getSignData(), base64.b64decode(self.__signature), pubKey, Defines.SIGNATURE_ALGO):
            raise IPC_Exception('Signature check failed!')

    def __getSignData(self):
        return base64.b64encode('-'.join(list(Helper.getValuesFromMultiDimensionalArray(self.__data))))


    @staticmethod
    def getInstance(cnf: Config, raw_data, format: str):
        """
    * Static class to create Response object\n
    * @param cnf: Config
    * @param string|array raw_data
    * @param string format\n
    * @return Response
    * @raises IPC_Exception
        """
        return Response(cnf, raw_data, format)

    def isSignatureCorrect(self):
        """
    * Validate Signature param from IPC response\n
    * @return boolean
        """
        try:
            self.__verifySignature()
        except Exception as ex:
            return False

        return True

    def getSignature(self):
        """
    * Request param: Signature\n
    * @return string
        """
        return self.__signature

    #############################################

    def getStatus(self):
        """
    * Request param: Status\n
    * @return int
    * @raises IPC_Exception
        """
        return Helper.getArrayVal(self.getData(str.lower), 'status')

    def getData(self, case = None):
        """
    * Return IPC Response in array\n
    * @param function case str.lower|str.upper\n
    * @return array
    * @raises IPC_Exception
        """
        if case != None:
            if (not case in [
                str.lower,
                str.upper,
            ]):
                raise IPC_Exception('Invalid Key Case!')

            return dict((case(k), v) for k, v in self.__data)
            # array_change_key_case(self.__data, case)

        return self.__data

    def getStatusMsg(self):
        """
    * Request param: StatusMsg\n
    * @return string
    * @raises IPC_Exception
        """
        return Helper.getArrayVal(self.getData(str.lower), 'statusmsg')

    def getDataRaw(self):
        """
    * Return IPC Response in original format json/xml/array\n
    * @return string|array
        """
        return self.__raw_data
