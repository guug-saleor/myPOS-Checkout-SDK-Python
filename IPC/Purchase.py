from IPC.Base import Base
from IPC.Cart import Cart
from IPC.Customer import Customer
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class Purchase(Base):
    """
 * Process IPC method: IPCPurchase.
 * Collect, validate and send API params
    """
    PURCHASE_TYPE_FULL = 1
    PURCHASE_TYPE_SIMPLIFIED_CALL = 2
    PURCHASE_TYPE_SIMPLIFIED_PAYMENT_PAGE = 3

    CARD_TOKEN_REQUEST_NONE = 0
    CARD_TOKEN_REQUEST_ONLY_STORE = 1
    CARD_TOKEN_REQUEST_PAY_AND_STORE = 2

    PAYMENT_METHOD_STANDARD = 1
    PAYMENT_METHOD_IDEAL = 2
    PAYMENT_METHOD_BOTH = 3

    __cart: Cart
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

    def __init__(self, cnf: Config):
        """
    * Return purchase object\n
    * @param cnf: Config
        """
        self.__paymentMethod = self.PAYMENT_METHOD_BOTH
        self._setCnf(cnf)

    def setOrderID(self, orderID: str):
        """
    * Purchase identifier - must be unique\n
    * @param string orderID\n
    * @return Purchase
        """
        self.__orderID = orderID

        return self

    def setNote(self, note: str):
        """
    * Optional note to purchase\n
    * @param string note\n
    * @return Purchase
        """
        self.__note = note

        return self

    def setUrlCancel(self, urlCancel: str):
        """
    * Merchant Site URL where client comes after unsuccessful payment\n
    * @param string urlCancel\n
    * @return Purchase
        """
        self.__url_cancel = urlCancel

        return self

    def setUrlNotify(self, urlNotify: str):
        """
    * Merchant Site URL where IPC posts Purchase Notify requests\n
    * @param string urlNotify\n
    * @return Purchase
        """
        self.__url_notify = urlNotify

        return self

    def setCardTokenRequest(self, cardTokenRequest: int):
        """
    * Whether to return Card Token for current client card\n
    * @param integer cardTokenRequest
        """
        self.__cardTokenRequest = cardTokenRequest

    def setPaymentParametersRequired(self, paymentParametersRequired: int):
        """
    * Defines the packet of details needed from merchant and client to make payment\n
    * @param integer paymentParametersRequired
        """
        self.__paymentParametersRequired = paymentParametersRequired

    def process(self):
        """
    * Initiate API request\n
    * @return boolean
    * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCPurchase')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

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
            self._getCnf().validate()
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
    * @return Purchase
        """
        self.__url_ok = urlOk

        return self

    def getCardTokenRequest(self):
        """
    * Whether to return Card Token for current client card\n
    * @return integer
        """
        return self.__cardTokenRequest

    def getPaymentParametersRequired(self):
        """
    * Defines the packet of details needed from merchant and client to make payment\n
    * @return integer
        """
        return self.__paymentParametersRequired

    def getCurrency(self):
        """
    * ISO-4217 Three letter __currency code\n
    * @return string
        """
        return self.__currency

    def setCurrency(self, currency: str):
        """
    * ISO-4217 Three letter __currency code\n
    * @param string currency\n
    * @return Purchase
        """
        self.__currency = currency

        return self

    def __isNoCartPurchase(self):
        """
    * If request is only for card token request without payment, the Amount and Cart params are not required\n
    * @return bool
        """
        return self.getCardTokenRequest() == self.CARD_TOKEN_REQUEST_ONLY_STORE

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
    * @return Purchase
        """
        self.__cart = cart

        return self

    def getCustomer(self):
        """
    * @return Customer
        """
        return self.__customer

    def setCustomer(self, customer: Customer):
        """
    * Customer object\n
    * @param customer: Customer\n
    * @return Purchase
        """
        self.__customer = customer

        return self

    def getOrderID(self):
        """
    * Purchase identifier\n
    * @return string
        """
        return self.__orderID

    def getNote(self):
        """
    * Optional note to purchase\n
    * @return string
        """
        return self.__note

    def getPaymentMethod(self):
        """
    * @return mixed
        """
        return self.__paymentMethod

    def setPaymentMethod(self, paymentMethod):
        """
    * @param mixed paymentMethod
        """
        self.__paymentMethod = paymentMethod
