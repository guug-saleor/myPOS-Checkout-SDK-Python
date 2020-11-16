from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class RequestMoney(Base):
    """
 * Process IPC method: IPCRequestMoney.
 * Collect, validate and send API params
    """
    __currency = 'EUR'
    __mandateReference: str
    __customerWalletNumber: str
    __reversalIndicator: bool
    __reason: str
    __orderID: str

    def __init__(self, cnf: Config):
        """
    * Return Refund object\n
    * @param cnf: Config
        """
        self._setCnf(cnf)

    def setAmount(self, amount: float):
        """
    * Refund amount\n
    * @param float amount
        """
        self.__amount = amount

    def setOrderID(self, orderID: str):
        """
    * Request identifier - must be unique\n
    * @param string orderID\n
    * @return RequestMoney
        """
        self.__orderID = orderID

        return self

    def setMandateReference(self, mandateReference: str):
        """
    * Unique identifier of the agreement (mandate) between the merchant and the client (debtor). Up to 127 characters.\n
    * @param string mandateReference
        """
        self.__mandateReference = mandateReference

    def setCustomerWalletNumber(self, customerWalletNumber: str):
        """
    * Identifier of the client’s (debtor’s) myPOS account\n
    * @param string customerWalletNumber
        """
        self.__customerWalletNumber = customerWalletNumber

    def setReversalIndicator(self, reversalIndicator: bool):
        """
    * Reversal of the previously executed Request money transaction.\n
    * @param bool reversalIndicator
        """
        self.__reversalIndicator = reversalIndicator

    def setReason(self, reason: str):
        """
    * The reason for the transfer.\n
    * @param string reason
        """
        self.__reason = reason

    def process(self):
        """
    * Initiate API request\n
    * @return Response
    * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCRequestMoney')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

        self._addPostParam('Currency', self.getCurrency())
        self._addPostParam('Amount', self.getAmount())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('MandateReference', self.getMandateReference())

        self._addPostParam('CustomerWalletNumber', self.getCustomerWalletNumber())
        self._addPostParam('ReversalIndicator', int(self.getReversalIndicator() | False))
        self._addPostParam('Reason', self.getReason())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    def validate(self):
        """
    * Validate all set refund details\n
    * @return boolean
    * @raises IPC_Exception
        """
        try:
            self._getCnf().validate()
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

    def getAmount(self):
        """
    * Refund amount\n
    * @return float
        """
        return self.__amount

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
    * @return RequestMoney
        """
        self.__currency = currency

        return self

    def getOrderID(self):
        """
    * Request identifier - must be unique\n
    * @return string
        """
        return self.__orderID

    def getMandateReference(self):
        """
    * Unique identifier of the agreement (mandate) between the merchant and the client (debtor). Up to 127 characters.\n
    * @return string
        """
        return self.__mandateReference

    def getCustomerWalletNumber(self):
        """
    * Identifier of the client’s (debtor’s) myPOS account\n
    * @return string
        """
        return self.__customerWalletNumber

    def getReversalIndicator(self):
        """
    * Reversal of the previously executed Request money transaction.\n
    * @return bool
        """
        return self.__reversalIndicator

    def getReason(self):
        """
    * The reason for the transfer.\n
    * @return string
        """
        return self.__reason
