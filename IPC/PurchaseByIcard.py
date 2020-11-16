from IPC.Base import Base
from IPC.Cart import Cart
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class PurchaseByIcard(Base):
    """
 * Process IPC method: IPCPurchaseByIcard.
 * Collect, validate and send API params
    """

    __cart: Cart

    __url_ok: str
    __url_cancel: str
    __url_notify: str
    __phone: str
    __email: str
    __currency = 'EUR'
    __orderID: str

    def __init__(self, cnf: Config):
        """
    * Return purchase object\n
    * @param cnf: Config
        """
        self._setCnf(cnf)

    def setOrderID(self, orderID: str):
        """
    * Purchase identifier - must be unique\n
    * @param string orderID\n
    * @return PurchaseByIcard
        """
        self.__orderID = orderID

        return self

    def getPhone(self):
        """
    * Customer Phone number\n
    * @return string
        """
        return self.__phone

    def setPhone(self, phone: str):
        """
    * Customer Phone number\n
    * @param string phone\n
    * @return PurchaseByIcard
        """
        self.__phone = phone

        return self

    def getEmail(self):
        """
    * Customer Email address\n
    * @return string
        """
        return self.__email

    def setEmail(self, email: str):
        """
    * Customer Email address\n
    * @param string email\n
    * @return PurchaseByIcard
        """
        self.__email = email

        return self

    def setUrlCancel(self, urlCancel: str):
        """
    * Merchant Site URL where client comes after unsuccessful payment\n
    * @param string urlCancel\n
    * @return PurchaseByIcard
        """
        self.__url_cancel = urlCancel

        return self

    def setUrlNotify(self, urlNotify: str):
        """
    * Merchant Site URL where IPC posts Purchase Notify requests\n
    * @param string urlNotify\n
    * @return PurchaseByIcard
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

        self._addPostParam('IPCmethod', 'IPCPurchaseByIcard')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

        self._addPostParam('Currency', self.getCurrency())
        self._addPostParam('Amount', self.__cart.getTotal())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('URL_OK', self.getUrlOk())
        self._addPostParam('URL_Cancel', self.getUrlCancel())
        self._addPostParam('URL_Notify', self.getUrlNotify())

        self._addPostParam('CustomerEmail', self.getEmail())
        self._addPostParam('CustomerPhone', self.getPhone())

        self._addPostParam('CartItems', self.__cart.getItemsCount())
        items = self.__cart.getCart()
        i = 1
        for v in items :
            self._addPostParam(f'Article_{i}', v['name'])
            self._addPostParam(f'Quantity_{i}', v['quantity'])
            self._addPostParam(f'Price_{i}', v['price'])
            self._addPostParam(f'Amount_{i}', v['price'] * v['quantity'])
            self._addPostParam(f'Currency_{i}', self.getCurrency())
            i += 1
        self._processHtmlPost()

        return True

    def validate(self):
        """
    * Validate all set purchase details\n
    * @return boolean
    * @raises IPC_Exception
        """
        if self.getUrlCancel() == None or not Helper.isValidURL(self.getUrlCancel()):
            raise IPC_Exception('Invalid Cancel URL')

        if self.getUrlNotify() == None or not Helper.isValidURL(self.getUrlNotify()):
            raise IPC_Exception('Invalid Notify URL')

        if self.getUrlOk() == None or not Helper.isValidURL(self.getUrlOk()):
            raise IPC_Exception('Invalid Success URL')

        if self.getCurrency() == None:
            raise IPC_Exception('Invalid currency')

        if self.getEmail() == None and self.getPhone()  == None :
            raise IPC_Exception('Must provide customer email either phone')

        if self.getEmail() != None and not Helper.isValidEmail(self.getEmail()):
            raise IPC_Exception('Invalid Email')

        try:
            self._getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getCart() == None:
            raise IPC_Exception('Missing Cart details')

        try:
            self.getCart().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Cart details: {ex}')

        return True

    def getUrlCancel(self):
        """
    * Merchant Site URL where client comes after unsuccessful payment\n
    * @return string
        """
        return self.__url_cancel

    def getUrlNotify(self):
        """
    * Merchant Site URL where IPC posts Purchase Notify requests\n
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
    * @return PurchaseByIcard
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
    * @return PurchaseByIcard
        """
        self.__currency = currency

        return self

    def getCart(self):
        """
    * Cart object\n
    * @return Cart
        """
        return self.__cart

    def setCart(self, cart: Cart):
        """
    * Cart object\n
    * @param cart: Cart\n
    * @return PurchaseByIcard
        """
        self.__cart = cart

        return self

    def getOrderID(self):
        """
    * Purchase identifier\n
    * @return string
        """
        return self.__orderID
