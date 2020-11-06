from .Base import Base
from .Config import Config
from .IPC_Exception import IPC_Exception

class Authorization(Base):

    __card = None
    __currency = 'EUR'
    __note = None
    __orderID = None
    __itemName = None
    __amount = None

    def __init__(self, cnf:Config):
        self.setCnf(cnf)

    def setOrderID(self, orderId):
        self.__orderID = orderId
        return self

    def setItemName(self, itemName):
        self.__itemName = itemName
        return self

    def setCurrency(self, cur):
        self.__currency = cur
        return self

    def setAmount(self, amount):
        self.__amount = amount
        return self

    def setCard(self, card):
        self.__card = card
        return self

    def setNote(self, note):
        self.__note = note
        return self

    def process(self):
        self.validate()

        cnf = self._getCnf()

        self._addPostParam('IPCmethod', 'IPCAuthorization')
        self._addPostParam('IPCVersion', cnf.getVersion())
        self._addPostParam('IPCLanguage', cnf.getLang())
        self._addPostParam('SID', cnf.getSid())
        self._addPostParam('WalletNumber', cnf.getWallet())
        self._addPostParam('KeyIndex', cnf.getKeyIndex())
        self._addPostParam('Source', cnf.getSource())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('ItemName', self.getItemName())

        self._addPostParam('Amount', self.getAmount())
        self._addPostParam('Currency', self.getCurrency())

        self._addPostParam('CardToken', self.getCard().getCardToken())

        self._addPostParam('Note', self.getNote())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    def validate(self):
        try:
            self._getCnf().validate()
        except IPC_Exception as ex:
            raise IPC_Exception('Invalid config details: {}'.format(str(ex)))

        if float(self._getCnf().getVersion()) < 1.4:
            raise IPC_Exception('IPCVersion {} does not support IPCAuthorization method. Please use 1.4 or above.'.format(self._getCnf().getVersion()))

        if self.getItemName() == None or not isinstance(self.getItemName(), str):
            raise IPC_Exception('Empty or invalid item name')

        if self.getCurrency() == None:
            raise IPC_Exception('Invalid currency')

        if self.getAmount() == None:
            raise IPC_Exception('Empty or Invalid amount')
        else:
            try:
                float(self.getAmount())
            except:
                raise IPC_Exception('Empty or Invalid amount')

        if self.getCard() == None:
            raise IPC_Exception('Missing card details')

        if self.getCard().getCardNumber() != None:
            raise IPC_Exception('IPCAuthorization supports only card token')

        try:
            self.getCard().validate()
        except IPC_Exception as ex:
            raise IPC_Exception('Invalid Card details: {}'.format(str(ex)))

        return True

    def getCurrency(self):
        return self.__currency

    def getCard(self):
        return self.__card

    def getOrderID(self):
        return self.__orderID

    def getItemName(self):
        return self.__itemName

    def getAmount(self):
        return self.__amount

    def getNote(self):
        return self.__note