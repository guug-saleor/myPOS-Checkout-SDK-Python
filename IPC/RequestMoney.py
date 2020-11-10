from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCRequestMoney.
 * Collect, validate and send API params
"""
class RequestMoney(Base):
    __currency = 'EUR'
    __mandateReference: str
    __customerWalletNumber: str
    __reversalIndicator: bool
    __reason: str
    __orderID: str

    """
    * Return Refund object
    *
    * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
    * Refund amount
    *
    * @param float amount
    """
    def setAmount(self, amount: float):
        self.__amount = amount

    """
    * Request identifier - must be unique
    *
    * @param string orderID
    *
    * @return RequestMoney
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * Unique identifier of the agreement (mandate) between the merchant and the client (debtor). Up to 127 characters.
    *
    * @param string mandateReference
    """
    def setMandateReference(self, mandateReference: str):
        self.__mandateReference = mandateReference

    """
    * Identifier of the client’s (debtor’s) myPOS account
    *
    * @param string customerWalletNumber
    """
    def setCustomerWalletNumber(self, customerWalletNumber: str):
        self.__customerWalletNumber = customerWalletNumber

    """
    * Reversal of the previously executed Request money transaction.
    *
    * @param bool reversalIndicator
    """
    def setReversalIndicator(self, reversalIndicator: bool):
        self.__reversalIndicator = reversalIndicator

    """
    * The reason for the transfer.
    *
    * @param string reason
    """
    def setReason(self, reason: str):
        self.__reason = reason

    """
    * Initiate API request
    *
    * @return Response
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCRequestMoney')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('Currency', self.getCurrency())
        self._addPostParam('Amount', self.getAmount())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('MandateReference', self.getMandateReference())

        self._addPostParam('CustomerWalletNumber', self.getCustomerWalletNumber())
        self._addPostParam('ReversalIndicator', int(self.getReversalIndicator() | False))
        self._addPostParam('Reason', self.getReason())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    """
    * Validate all set refund details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getAmount() == None or not Helper.isValidAmount(self.getAmount()):
            raise IPC_Exception('Invalid Amount')

        if self.getCurrency() == None:
            raise IPC_Exception('Invalid Currency')

        if self.getOrderID() == None or not Helper.isValidOrderId(self.getOrderID()):
            raise IPC_Exception('Invalid OrderId')

        if self.getOutputFormat() == None or not Helper.isValidOutputFormat(self.getOutputFormat()):
            raise IPC_Exception('Invalid Output format')

        return True

    """
    * Refund amount
    *
    * @return float
    """
    def getAmount(self):
        return self.__amount

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
    * @return RequestMoney
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self

    """
    * Request identifier - must be unique
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID

    """
    * Unique identifier of the agreement (mandate) between the merchant and the client (debtor). Up to 127 characters.
    *
    * @return string
    """
    def getMandateReference(self):
        return self.__mandateReference

    """
    * Identifier of the client’s (debtor’s) myPOS account
    *
    * @return string
    """
    def getCustomerWalletNumber(self):
        return self.__customerWalletNumber

    """
    * Reversal of the previously executed Request money transaction.
    *
    * @return bool
    """
    def getReversalIndicator(self):
        return self.__reversalIndicator

    """
    * The reason for the transfer.
    *
    * @return string
    """
    def getReason(self):
        return self.__reason
