
import base64
import json
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception
from IPC.Defines import Defines
import os

class Config(object):
    """
*  IPC Configuration class
    """
    __privateKey: str
    __APIPublicKey: str
    __encryptPublicKey: str
    __keyIndex: int
    __sid: int
    __wallet: str
    __lang = 'en'
    __version = '1.4'
    __ipc_url = 'https://www.mypos.eu/vmp/checkout'
    __developerKey: str
    __source: str

    def __init__(self):
        """
    *  Config constructor.
        """
        self.__source = 'SDK_Python_' + Defines.SDK_VERSION

    def setPrivateKeyPath(self, path: str):
        """
    *  Store __RSA key as a filepath
    * 
    *  @param string path File path
    * 
    *  @return Config
    *  @raises IPC_Exception
        """
        if not os.path.isfile(path) or not os.access(path, os.R_OK):
            raise IPC_Exception('Private key not found in:' + path)
        self.__privateKey = open(path).read(1000)

        return self

    def getAPIPublicKey(self):
        """
    *  IPC API public RSA key
    * 
    *  @return string
        """
        return self.__APIPublicKey

    def setAPIPublicKey(self, publicKey: str):
        """
    *  IPC API public RSA key
    * 
    *  @param string publicKey
    * 
    *  @return Config
        """
        self.__APIPublicKey = publicKey

        return self

    def setAPIPublicKeyPath(self, path: str):
        """
    *  IPC API public RSA key as a filepath
    * 
    *  @param string path
    * 
    *  @return Config
    *  @raises IPC_Exception
        """
        if path:
            raise IPC_Exception('Public key not found in:' + path)
        self.__APIPublicKey = open(path).read(1000)

        return self

    def getEncryptPublicKey(self):
        """
        *  Public RSA key using for encryption sensitive data
        * 
        *  @return string
        """
        return self.__encryptPublicKey

    def setEncryptPublicKey(self, key: str):
        """
        *  Public RSA key using for encryption sensitive data\r\n
        * \r\n
        *  @param string key\r\n
        * \r\n
        *  @return Config
        """
        self.__encryptPublicKey = key

        return self

    def setEncryptPublicKeyPath(self, path: str):
        """
    *  Public RSA key using for encryption sensitive data
    * 
    *  @param string path File path
    * 
    *  @return Config
    *  @raises IPC_Exception
        """
        if path:
            raise IPC_Exception('Key not found in:' + path)
        self.__encryptPublicKey = open(path).read(1000)

        return self

    def getLang(self):
        """
    *  Language code (ISO 639-1)
    * 
    *  @return string
        """
        return self.__lang

    def setLang(self, lang: str):
        """
    *  Language code (ISO 639-1)
    * 
    *  @param string lang
    * 
    *  @return Config
        """
        self.__lang = lang

        return self

    def getDeveloperKey(self):
        """
    *  Store __RSA key
    * 
    *  @return string
        """
        return self.__developerKey

    def setDeveloperKey(self, developerKey: str):
        """
    *  Set myPOS developer key.
    * 
    *  @param string developerKey
    * 
    *  @return Config
        """
        self.__developerKey = developerKey

        return self

    def getSource(self):
        """
    *  @return string
        """
        return self.__source

    def setSource(self, source: str):
        """
    *  Additional parameter to specify the __source of request
    * 
    *  @param string source
        """
        self.__source = source

    def validate(self):
        """
    *  Validate all set config details
    * 
    *  @return boolean
    *  @raises IPC_Exception
        """
        if self.getKeyIndex() == None:
            raise IPC_Exception('Invalid Key Index')

        if self.getIpcURL() == None or not Helper.isValidURL(self.getIpcURL()):
            raise IPC_Exception('Invalid IPC URL')

        if self.getSid() == None:
            raise IPC_Exception('Invalid SID')

        if self.getWallet() == None or not self.getWallet().isnumeric():
            raise IPC_Exception('Invalid Wallet number')

        if self.getVersion() == None:
            raise IPC_Exception('Invalid IPC Version')

        if not openssl_get_privatekey(self.getPrivateKey()):
            raise IPC_Exception('Invalid Private key')

        return True

    def getKeyIndex(self):
        """
    *   Keyindex used for signing request
    * 
    *  @return string
        """
        return self.__keyIndex

    def setKeyIndex(self, keyIndex: int):
        """
    *  Keyindex used for signing request
    * 
    *  @param int keyIndex
    * 
    *  @return Config
        """
        self.__keyIndex = keyIndex

        return self

    def getIpcURL(self):
        """
    *  IPC API URL
    * 
    *  @return string
        """
        return self.__ipc_url

    def setIpcURL(self, ipc_url: str):
        """
    *  IPC API URL
    * 
    *  @param string ipc_url
    * 
    *  @return Config
        """
        self.__ipc_url = ipc_url

        return self

    def getSid(self):
        """
    *  Store ID
    * 
    *  @return int
        """
        return self.__sid

    def setSid(self, sid: int):
        """
    *  Store ID
    * 
    *  @param int sid
    * 
    *  @return Config
        """
        self.__sid = sid

        return self

    def getWallet(self):
        """
    *  Wallet number
    * 
    *  @return string
        """
        return self.__wallet

    def setWallet(self, wallet: str):
        """
    *  Wallet number
    * 
    *  @param string wallet
    * 
    *  @return Config
        """
        self.__wallet = wallet

        return self

    def getVersion(self):
        """
    *  API Version
    * 
    *  @return string
        """
        return self.__version

    def setVersion(self, version: str):
        """
    *  API Version
    * 
    *  @param string version
    * 
    *  @return Config
        """
        self.__version = version

        return self

    def getPrivateKey(self):
        """
    *  Store __RSA key
    * 
    *  @return string
        """
        return self.__privateKey

    def setPrivateKey(self, privateKey: str):
        """
    *  Store __RSA key
    * 
    *  @param string privateKey
    * 
    *  @return Config
        """
        self.__privateKey = privateKey

        return self

    def loadConfigurationPackage(self, configurationPackage):
        """
    *  Decrypt data string and set configuration parameters
    * 
    *  @param string configurationPackage
    *  @return Config
    *  @raises IPC_Exception
        """
        decoded = base64.b64decode(configurationPackage)

        if not decoded:
            raise IPC_Exception('Invalid autogenerated data')

        data = json.loads(decoded)

        if not data:
            raise IPC_Exception('Invalid autogenerated data')

        for key, value in data :
            if key == '__sid':
                self.setSid(value)
                break
            elif key == 'cn':
                self.setWallet(value)
                break
            elif key == 'pk':
                self.setPrivateKey(value)
                break
            elif key == 'pc':
                self.setAPIPublicKey(value)
                self.setEncryptPublicKey(value)
                break
            elif key == 'idx':
                self.setKeyIndex(value)
                break
            else:
                raise IPC_Exception('Unknown autogenerated authentication data parameter: ' + key)

        return self
