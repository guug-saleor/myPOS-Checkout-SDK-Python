from abc import ABC, abstractmethod
from .Defines import Defines
from .Config import Config
from . import Crypto

import urllib

import base64

class Base(ABC):

    outputFormat = Defines.COMMUNICATION_FORMAT_JSON

    __cnf : Config
    __params = {}

    @staticmethod
    def isValidSignature(data, signature, pubKey):
        return Crypto.verify(data, signature, pubKey)

    def getOutputFormat(self):
        return self.outputFormat

    def setOutputFormat(self, format):
        self.outputFormat = format

    def _addPostParam(self, name, value, encrypt=False):
        self.__params[name] = self.encryptData(value) if encrypt else Helper.escape(value)

    def __encryptData(self, data):
        return base64.b64encode(Crypto.encrypt(data, self._getCnf().getEncryptPublicKey()))

    def _getCnf(self):
        return self.__cnf

    def _setCnf(self, cnf:Config):
        self.__cnf = cnf

    def __prepareHtmlPost(self):
        self.__params['Signature'] = self._createSignature()
        c += '<body onload="document.ipcForm.submit();">'
        c += '<form id="ipcForm" name="ipcForm" action="{}" method="post">'.format(self._getCnf().getIpcURL())
        for k, v in enumerate(self.__params):
            c += "<input type=\"hidden\" name=\"\" value=\"\"  />\n".format(k,v)
        c += '</form></body>'
        return c

    def _createSignature(self):
        params = self.__params
        for k, v in enumerate(self.params):
            params[k] = Helper.escape(v)

        concData = base64.b64encode("-".join(params))
        privKey = self._getCnf().getPrivateKey()
        signature = Crypto.sign(concData, privKey, Defines.SIGNATURE_ALGO)

        return base64.b64encode(signature)

    def _processPost(self):
        self.__params['Signature'] = self._createSignature()
        url = urllib.parse.urlparse(self._getCnf().getIpcURL())
        ssl = ''
        '''if url.port:
            if url.scheme == 'https':
                url.port = 443
                ssl = 'ssl://'
            else:
                url.port = 80'''

        postData = urllib.parse.urlencode(self.__params).encode()
        request = urllib.request.Request(url, data=postData)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError:
            raise IPC_Exception('Error connecting IPC URL')
        cont = response.body.strip()


        return Response.getInstance(self._getCnf(), cont, self.outputFormat)

    def __is_hex(self, hex):
        try:
            int(hex, 16)
            return True
        except:
            return False