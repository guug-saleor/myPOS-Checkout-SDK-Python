from IPC.Base import Base
from IPC.Card import Card
from IPC.Cart import Cart
from IPC.Config import Config
from IPC.IPC_Exception import IPC_Exception


class IAPurchase(Base):
    """
 * Process IPC method: IPCIAPurchase.
 * Collect, validate and send API params
    """

    __cart: Cart

    __card: Card
    __currency = 'EUR'
    __accountSettlement: str
    __orderID: str
    __note: str

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
    * @return IAPurchase
        """
        self.__orderID = orderID

        return self

    def setNote(self, note: str):
        """
    * Optional note to purchase\n
    * @param string note\n
    * @return IAPurchase
        """
        self.__note = note

        return self

    def setAccountSettlement(self, accountSettlement: str):
        """
    * Account for payment settlement\n
    * @param string accountSettlement
        """
        self.__accountSettlement = accountSettlement

    def process(self):
        """
    * Initiate API request\n
    * @return Response
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCIAPurchase')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

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

    def validate(self):
        """
    * Validate all set purchase details\n
    * @return boolean
    * @raises IPC_Exception
        """
        if self.getCurrency() == None:
            raise IPC_Exception('Invalid currency')

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

        if self.getCart() == None:
            raise IPC_Exception('Missing card details')

        try:
            self.getCard().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Card details: {ex}')

        return True

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
    * @return IAPurchase
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
    * @return IAPurchase
        """
        self.__cart = cart

        return self

    def getCard(self):
        """
    * Card object\n
    * @return Card
        """
        return self.__card

    def setCard(self, card: Card):
        """
    * Card object\n
    * @param Card card
        """
        self.__card = card

    def getOrderID(self):
        """
    * Purchase identifier\n
    * @return string
        """
        return self.__orderID

    def getAccountSettlement(self):
        """
    * Account for payment settlement\n
    * @return string
        """
        return self.__accountSettlement

    def getNote(self):
        """
    * Optional note to purchase\n
    * @return string
        """
        return self.__note
