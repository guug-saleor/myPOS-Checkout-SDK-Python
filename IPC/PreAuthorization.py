from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class PreAuthorization(Base):
    """
 * Process IPC method: IPCPreAuthorization.
 * Collect, validate and send API params
    """
    __url_ok: str
    __url_cancel: str
    __url_notify: str
    __currency = 'EUR'
    __amount: float
    __itemName: str
    __orderID: str
    __note: str

    def __init__(self, cnf: Config):
        """
    * Return PreAuthorization object\n
    * @param cnf: Config
        """
        self._setCnf(cnf)

    def setOrderID(self, orderID: str):
        """
    * PreAuthorization identifier - must be unique\n
    * @param string orderID\n
    * @return PreAuthorization
        """
        self.__orderID = orderID

        return self

    def setItemName(self, itemName: str):
        """
    * @param string itemName\n
    * @return PreAuthorization
        """
        self.__itemName = itemName

        return self

    def setAmount(self, amount: float):
        """
    * Total amount of the PreAuthorization\n
    * @param float amount\n
    * @return PreAuthorization
        """
        self.__amount = amount

        return self


    def setNote(self, note: str):
        """
    * Optional note for PreAuthorization\n
    * @param string note\n
    * @return PreAuthorization
        """
        self.__note = note

        return self

    def setUrlCancel(self, urlCancel: str):
        """
    * Merchant Site URL where client comes after unsuccessful payment\n
    * @param string urlCancel\n
    * @return PreAuthorization
        """
        self.__url_cancel = urlCancel

        return self

    def setUrlNotify(self, urlNotify: str):
        """
    * Merchant Site URL where IPC posts PreAuthorization Notify requests\n
    * @param string urlNotify\n
    * @return PreAuthorization
        """
        self.__url_notify = urlNotify

        return self

    def process(self):
        """
    * Initiate API request\n
    * @return boolean
    * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCPreAuthorization')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

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

    def validate(self):
        """
    * Validate all set PreAuthorization details\n
    * @return boolean
    * @raises IPC_Exception
        """
        if not Helper.versionCheck(self._getCnf().getVersion(), '1.4'):
            raise IPC_Exception('IPCVersion ' + self._getCnf().getVersion() + ' does not support IPCPreAuthorization method. Please use 1.4 or above.')

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
            raise IPC_Exception('Invalid currency')

        try:
            self._getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        return True

    def getUrlCancel(self):
        """
    * Merchant Site URL where client comes after unsuccessful payment\n
    * @return string
        """
        return self.__url_cancel

    def getUrlNotify(self):
        """
    * Merchant Site URL where IPC posts PreAuthorization Notify requests\n
    * @var string
        """
        return self.__url_notify

    def getUrlOk(self):
        """
    * Merchant Site URL where client comes after successful payment\n
    * @return string
        """
        return self.__url_ok

    def setUrlOk(self, urlOk: str):
        """
    * Merchant Site URL where client comes after successful payment\n
    * @param string urlOk\n
    * @return PreAuthorization
        """
        self.__url_ok = urlOk

        return self

    def getCurrency(self):
        """
    * ISO-4217 Three letter currency code\n
    * @return string
        """
        return self.__currency

    def setCurrency(self, currency: str):
        """
    * ISO-4217 Three letter currency code\n
    * @param string currency\n
    * @return PreAuthorization
        """
        self.__currency = currency

        return self


    def getOrderID(self):
        """
    * PreAuthorization identifier\n
    * @return string
        """
        return self.__orderID

    def getItemName(self):
        """
    * @return string
        """
        return self.__itemName

    def getAmount(self):
        """
    * Total amount of the PreAuthorization\n
    * @return float
        """
        return self.__amount

    def getNote(self):
        """
    * Optional note to PreAuthorization\n
    * @return string
        """
        return self.__note
