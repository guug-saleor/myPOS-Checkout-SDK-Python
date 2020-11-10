from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCPreAuthorization.
 * Collect, validate and send API params
"""
class PreAuthorization(Base):
    """
    * @var Customer
    """
    __url_ok: str
    __url_cancel: str
    __url_notify: str
    __currency = 'EUR'
    __amount: float
    __itemName: str
    __orderID: str
    __note: str

    """
    * Return PreAuthorization object
    *
    * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
    * PreAuthorization identifier - must be unique
    *
    * @param string orderID
    *
    * @return PreAuthorization
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * @param string itemName
    *
    * @return PreAuthorization
    """
    def setItemName(self, itemName: str):
        self.__itemName = itemName

        return self

    """
    * Total amount of the PreAuthorization
    *
    * @param float amount
    *
    * @return PreAuthorization
    """
    def setAmount(self, amount: float):
        self.__amount = amount

        return self


    """
    * Optional note for PreAuthorization
    *
    * @param string note
    *
    * @return PreAuthorization
    """
    def setNote(self, note: str):
        self.__note = note

        return self

    """
    * Merchant Site URL where client comes after unsuccessful payment
    *
    * @param string urlCancel
    *
    * @return PreAuthorization
    """
    def setUrlCancel(self, urlCancel: str):
        self.__url_cancel = urlCancel

        return self

    """
    * Merchant Site URL where IPC posts PreAuthorization Notify requests
    *
    * @param string urlNotify
    *
    * @return PreAuthorization
    """
    def setUrlNotify(self, urlNotify: str):
        self.__url_notify = urlNotify

        return self

    """
    * Initiate API request
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCPreAuthorization')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('ItemName', self.getItemName())

        self._addPostParam('Currency', self.getCurrency())
        self._addPostParam('Amount', self.getAmount())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('URL_OK', self.getUrlOk())
        self._addPostParam('URL_Cancel', self.getUrlCancel())
        self._addPostParam('URL_Notify', self.getUrlNotify())

        self._addPostParam('Note', self.getNote())

        self._processHtmlPost()

        return True

    """
    * Validate all set PreAuthorization details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        if not Helper.versionCheck(self.getCnf().getVersion(), '1.4'):
            raise IPC_Exception('IPCVersion ' + self.getCnf().getVersion() + ' does not support IPCPreAuthorization method. Please use 1.4 or above.')

        if self.getItemName() == None or not isinstance(self.getItemName(), str):
            raise IPC_Exception('Empty or invalid item name.')

        if self.getUrlCancel() == None or not Helper.isValidURL(self.getUrlCancel()):
            raise IPC_Exception('Invalid Cancel URL')

        if (self.getUrlNotify() == None or not Helper.isValidURL(self.getUrlNotify())):
            raise IPC_Exception('Invalid Notify URL')

        if self.getUrlOk() == None or not Helper.isValidURL(self.getUrlOk()):
            raise IPC_Exception('Invalid Success URL')

        if self.getAmount() == None or not Helper.isValidAmount(self.getAmount()):
            raise IPC_Exception('Empty or invalid amount')

        if self.getCurrency()  == None:
            raise IPC_Exception('Invalid __currency')

        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        return True

    """
    * Merchant Site URL where client comes after unsuccessful payment
    *
    * @return string
    """
    def getUrlCancel(self):
        return self.__url_cancel

    """
    * Merchant Site URL where IPC posts PreAuthorization Notify requests
    *
    * @var string
    """
    def getUrlNotify(self):
        return self.__url_notify

    """
    * Merchant Site URL where client comes after successful payment
    *
    * @return string
    """
    def getUrlOk(self):
        return self.__url_ok

    """
    * Merchant Site URL where client comes after successful payment
    *
    * @param string urlOk
    *
    * @return PreAuthorization
    """
    def setUrlOk(self, urlOk: str):
        self.__url_ok = urlOk

        return self

    """
    * ISO-4217 Three letter __currency code
    *
    * @return string
    """
    def getCurrency(self):
        return self.__currency

    """
    * ISO-4217 Three letter __currency code
    *
    * @param string currency
    *
    * @return PreAuthorization
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self


    """
    * PreAuthorization identifier
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID

    """
    * @return string
    """
    def getItemName(self):
        return self.__itemName

    """
    * Total amount of the PreAuthorization
    *
    * @return float
    """
    def getAmount(self):
        return self.__amount

    """
    * Optional note to PreAuthorization
    *
    * @return string
    """
    def getNote(self):
        return self.__note
