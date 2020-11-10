from IPC.Base import Base
from IPC.Cart import Cart
from IPC.Customer import Customer
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCPurchase.
 * Collect, validate and send API params
"""
class Purchase(Base):
    PURCHASE_TYPE_FULL = 1
    PURCHASE_TYPE_SIMPLIFIED_CALL = 2
    PURCHASE_TYPE_SIMPLIFIED_PAYMENT_PAGE = 3

    CARD_TOKEN_REQUEST_NONE = 0
    CARD_TOKEN_REQUEST_ONLY_STORE = 1
    CARD_TOKEN_REQUEST_PAY_AND_STORE = 2

    PAYMENT_METHOD_STANDARD = 1
    PAYMENT_METHOD_IDEAL = 2
    PAYMENT_METHOD_BOTH = 3
    """
    * @var Cart
    """
    __cart: Cart
    """
    * @var Customer
    """
    __customer: Customer
    __url_ok: str
    __url_cancel: str
    __url_notify: str
    __currency = 'EUR'
    __cardTokenRequest: int
    __paymentParametersRequired: int
    __orderID: str
    __note: str
    __paymentMethod = None

    """
    * Return purchase object
    *
    * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self.__paymentMethod = self.PAYMENT_METHOD_BOTH
        self._setCnf(cnf)

    """
    * Purchase identifier - must be unique
    *
    * @param string orderID
    *
    * @return Purchase
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * Optional note to purchase
    *
    * @param string note
    *
    * @return Purchase
    """
    def setNote(self, note: str):
        self.__note = note

        return self

    """
    * Merchant Site URL where client comes after unsuccessful payment
    *
    * @param string urlCancel
    *
    * @return Purchase
    """
    def setUrlCancel(self, urlCancel: str):
        self.__url_cancel = urlCancel

        return self

    """
    * Merchant Site URL where IPC posts Purchase Notify requests
    *
    * @param string urlNotify
    *
    * @return Purchase
    """
    def setUrlNotify(self, urlNotify: str):
        self.__url_notify = urlNotify

        return self

    """
    * Whether to return Card Token for current client card
    *
    * @param integer cardTokenRequest
    """
    def setCardTokenRequest(self, cardTokenRequest: int):
        self.__cardTokenRequest = cardTokenRequest

    """
    * Defines the packet of details needed from merchant and client to make payment
    *
    * @param integer paymentParametersRequired
    """
    def setPaymentParametersRequired(self, paymentParametersRequired: int):
        self.__paymentParametersRequired = paymentParametersRequired

    """
    * Initiate API request
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCPurchase')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('Currency', self.getCurrency())
        if self.__isNoCartPurchase():
            self._addPostParam('Amount', self.__cart.getTotal())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('URL_OK', self.getUrlOk())
        self._addPostParam('URL_Cancel', self.getUrlCancel())
        self._addPostParam('URL_Notify', self.getUrlNotify())

        self._addPostParam('Note', self.getNote())

        if self.getPaymentParametersRequired() != self.PURCHASE_TYPE_SIMPLIFIED_PAYMENT_PAGE:
            self._addPostParam('customeremail', self.getCustomer().getEmail())
            self._addPostParam('customerphone', self.getCustomer().getPhone())
            self._addPostParam('customerfirstnames', self.getCustomer().getFirstName())
            self._addPostParam('customerfamilyname', self.getCustomer().getLastName())
            self._addPostParam('customercountry', self.getCustomer().getCountry())
            self._addPostParam('customercity', self.getCustomer().getCity())
            self._addPostParam('customerzipcode', self.getCustomer().getZip())
            self._addPostParam('customeraddress', self.getCustomer().getAddress())

        if self.__isNoCartPurchase():
            self._addPostParam('CartItems', self.__cart.getItemsCount())
            items = self.__cart.getCart()
            i = 1
            for v in items :
                self._addPostParam(f'Article_{i}', v['name'])
                self._addPostParam(f'Quantity_{i}', v['quantity'])
                self._addPostParam(f'Price_{i}', v['price'])
                self._addPostParam(f'Amount_{i}', v['price'] * v['quantity'])
                self._addPostParam(f'Currency_{i}', self.getCurrency())
                if bool(v['delivery']):
                    self._addPostParam(f'Delivery_{i}', v['delivery'])

                i += 1

        self._addPostParam('CardTokenRequest', self.getCardTokenRequest())
        self._addPostParam('PaymentParametersRequired', self.getPaymentParametersRequired())
        self._addPostParam('PaymentMethod', self.getPaymentMethod())

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

        if (self.getCardTokenRequest() == None or (not self.getCardTokenRequest() in [
                self.CARD_TOKEN_REQUEST_NONE,
                self.CARD_TOKEN_REQUEST_ONLY_STORE,
                self.CARD_TOKEN_REQUEST_PAY_AND_STORE,
            ])):
            raise IPC_Exception('Invalid value provided for CardTokenRequest params')

        if (self.getPaymentParametersRequired() == None or (not self.getPaymentParametersRequired() in [
                self.PURCHASE_TYPE_FULL,
                self.PURCHASE_TYPE_SIMPLIFIED_CALL,
                self.PURCHASE_TYPE_SIMPLIFIED_PAYMENT_PAGE,
            ])):
            raise IPC_Exception('Invalid value provided for PaymentParametersRequired params')

        if self.getCurrency() == None:
            raise IPC_Exception('Invalid __currency')

        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if not self.__isNoCartPurchase():
            if self.getCart() == None:
                raise IPC_Exception('Missing Cart details')

            try:
                self.getCart().validate()
            except Exception as ex:
                raise IPC_Exception(f'Invalid Cart details: {ex}')

        if self.getPaymentParametersRequired() == self.PURCHASE_TYPE_FULL:
            try:
                if not self.getCustomer():
                    raise IPC_Exception('Customer details not set!')
                self.getCustomer().validate(self.getPaymentParametersRequired())
            except Exception as ex:
                raise IPC_Exception(f'Invalid Customer details: {ex}')

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
    * @return Purchase
    """
    def setUrlOk(self, urlOk: str):
        self.__url_ok = urlOk

        return self

    """
    * Whether to return Card Token for current client card
    *
    * @return integer
    """
    def getCardTokenRequest(self):
        return self.__cardTokenRequest

    """
    * Defines the packet of details needed from merchant and client to make payment
    *
    * @return integer
    """
    def getPaymentParametersRequired(self):
        return self.__paymentParametersRequired

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
    * @return Purchase
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self

    """
    * If request is only for card token request without payment, the Amount and Cart params are not required
    *
    * @return bool
    """
    def __isNoCartPurchase(self):
        return self.getCardTokenRequest() == self.CARD_TOKEN_REQUEST_ONLY_STORE

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
    * @return Purchase
    """
    def setCart(self, cart: Cart):
        self.__cart = cart

        return self

    """
    * @return Customer
    """
    def getCustomer(self):
        return self.__customer

    """
    * Customer object
    *
    * @param customer: Customer
    *
    * @return Purchase
    """
    def setCustomer(self, customer: Customer):
        self.__customer = customer

        return self

    """
    * Purchase identifier
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID

    """
    * Optional note to purchase
    *
    * @return string
    """
    def getNote(self):
        return self.__note

    """
    * @return mixed
    """
    def getPaymentMethod(self):
        return self.__paymentMethod

    """
    * @param mixed paymentMethod
    """
    def setPaymentMethod(self, paymentMethod):
        self.__paymentMethod = paymentMethod
