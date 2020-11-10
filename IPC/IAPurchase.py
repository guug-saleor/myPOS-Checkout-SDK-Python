from IPC.Base import Base
from IPC.Card import Card
from IPC.Cart import Cart
from IPC.Config import Config
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCIAPurchase.
 * Collect, validate and send API params
"""
class IAPurchase(Base):
    """
    * @var Cart
    """
    __cart: Cart
    """
    * @var Card
    """
    __card: Card
    __currency = 'EUR'
    __accountSettlement: str
    __orderID: str
    __note: str

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
    * @return IAPurchase
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * Optional note to purchase
    *
    * @param string note
    *
    * @return IAPurchase
    """
    def setNote(self, note: str):
        self.__note = note

        return self

    """
    * Account for payment settlement
    *
    * @param string accountSettlement
    """
    def setAccountSettlement(self, accountSettlement: str):
        self.__accountSettlement = accountSettlement

    """
    * Initiate API request
    *
    * @return Response
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCIAPurchase')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('Amount', self.getCart().getTotal())
        self._addPostParam('Currency', self.getCurrency())

        if self.getCard().getCardToken():
            self._addPostParam('CardToken', self.getCard().getCardToken())
        else:
            self._addPostParam('CardType', self.getCard().getCardType())
            self._addPostParam('PAN', self.getCard().getCardNumber(), True)
            self._addPostParam('CardholderName', self.getCard().getCardHolder())
            self._addPostParam('ExpDate', self.getCard().getExpDate(), True)
            self._addPostParam('CVC', self.getCard().getCvc(), True)
            self._addPostParam('ECI', self.getCard().getEci())
            self._addPostParam('AVV', self.getCard().getAvv())
            self._addPostParam('XID', self.getCard().getXid())

        self._addPostParam('AccountSettlement', self.getAccountSettlement())
        self._addPostParam('Note', self.getNote())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        self._addPostParam('CartItems', self.getCart().getItemsCount())
        items = self.getCart().getCart()
        i = 1
        for v in items :
            self._addPostParam(f'Article_{i}', v['name'])
            self._addPostParam(f'Quantity_{i}', v['quantity'])
            self._addPostParam(f'Price_{i}', v['price'])
            self._addPostParam(f'Amount_{i}', v['price'] * v['quantity'])
            self._addPostParam(f'Currency_{i}', self.getCurrency())
            i += 1

        return self._processPost()

    """
    * Validate all set purchase details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        if self.getCurrency() == None:
            raise IPC_Exception('Invalid __currency')

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

        if self.getCart() == None:
            raise IPC_Exception('Missing card details')

        try:
            self.getCard().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Card details: {ex}')

        return True

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
    * @return IAPurchase
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
    * @return IAPurchase
    """
    def setCart(self, cart: Cart):
        self.__cart = cart

        return self

    """
    * Card object
    *
    * @return Card
    """
    def getCard(self):
        return self.__card

    """
    * Card object
    *
    * @param Card card
    """
    def setCard(self, card: Card):
        self.__card = card

    """
    * Purchase identifier
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID

    """
    * Account for payment settlement
    *
    * @return string
    """
    def getAccountSettlement(self):
        return self.__accountSettlement

    """
    * Optional note to purchase
    *
    * @return string
    """
    def getNote(self):
        return self.__note
