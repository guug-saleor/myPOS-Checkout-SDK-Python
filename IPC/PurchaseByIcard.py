from IPC.Base import Base
from IPC.Cart import Cart
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCPurchaseByIcard.
 * Collect, validate and send API params
"""
class PurchaseByIcard(Base):
    """
    * @var Cart
    """
    __cart: Cart

    __url_ok: str
    __url_cancel: str
    __url_notify: str
    __phone: str
    __email: str
    __currency = 'EUR'
    __orderID: str

    """
    * Return purchase object
    *
    * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
    * Purchase identifier - must be unique
    *
    * @param string orderID
    *
    * @return PurchaseByIcard
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * Customer Phone number
    *
    * @return string
    """
    def getPhone(self):
        return self.__phone

    """
    * Customer Phone number
    *
    * @param string phone
    *
    * @return PurchaseByIcard
    """
    def setPhone(self, phone: str):
        self.__phone = phone

        return self

    """
    * Customer Email address
    *
    * @return string
    """
    def getEmail(self):
        return self.__email

    """
    * Customer Email address
    *
    * @param string email
    *
    * @return PurchaseByIcard
    """
    def setEmail(self, email: str):
        self.__email = email

        return self

    """
    * Merchant Site URL where client comes after unsuccessful payment
    *
    * @param string urlCancel
    *
    * @return PurchaseByIcard
    """
    def setUrlCancel(self, urlCancel: str):
        self.__url_cancel = urlCancel

        return self

    """
    * Merchant Site URL where IPC posts Purchase Notify requests
    *
    * @param string urlNotify
    *
    * @return PurchaseByIcard
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

        self._addPostParam('IPCmethod', 'IPCPurchaseByIcard')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

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

    """
    * Validate all set purchase details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):

        if self.getUrlCancel() == None or not Helper.isValidURL(self.getUrlCancel()):
            raise IPC_Exception('Invalid Cancel URL')

        if self.getUrlNotify() == None or not Helper.isValidURL(self.getUrlNotify()):
            raise IPC_Exception('Invalid Notify URL')

        if self.getUrlOk() == None or not Helper.isValidURL(self.getUrlOk()):
            raise IPC_Exception('Invalid Success URL')

        if self.getCurrency() == None:
            raise IPC_Exception('Invalid __currency')

        if self.getEmail() == None and self.getPhone()  == None :
            raise IPC_Exception('Must provide customer email either phone')

        if self.getEmail() != None and not Helper.isValidEmail(self.getEmail()):
            raise IPC_Exception('Invalid Email')

        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getCart() == None:
            raise IPC_Exception('Missing Cart details')

        try:
            self.getCart().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Cart details: {ex}')

        return True

    """
    * Merchant Site URL where client comes after unsuccessful payment
    *
    * @return string
    """
    def getUrlCancel(self):
        return self.__url_cancel

    """
    * Merchant Site URL where IPC posts Purchase Notify requests
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
    * @return PurchaseByIcard
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
    * @return PurchaseByIcard
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self

    """
    * Cart object
    *
    * @return Cart
    """
    def getCart(self):
        return self.__cart

    """
    * Cart object
    *
    * @param cart: Cart
    *
    * @return PurchaseByIcard
    """
    def setCart(self, cart: Cart):
        self.__cart = cart

        return self

    """
    * Purchase identifier
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID
