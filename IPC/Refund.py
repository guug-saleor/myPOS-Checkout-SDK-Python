from IPC.Base import Base
from IPC.Config import Config
from IPC.Defines import Defines
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCRefund.
 * Collect, validate and send API params
"""
class Refund(Base):
    __currency = 'EUR'
    __orderID: str
    __trnref = None
    __amount: float

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
    * Transaction reference - transaction unique identifier
    *
    * @param string trnref
    *
    * @return Refund
    """
    def setTrnref(self, trnref: str):
        self.__trnref = trnref

        return self

    """
    * Request identifier - must be unique
    *
    * @param string orderID
    *
    * @return Refund
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * Initiate API request
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCRefund')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('Currency', self.getCurrency())
        self._addPostParam('Amount', self.getAmount())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('IPC_Trnref', self.getTrnref())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        response = self._processPost().getData(str.lower)
        if (
            not response.get('ipc_trnref')
            or (not response['amount'] or response['amount'] != self.getAmount()) 
            or (not response['currency'] or response['currency'] != self.getCurrency()) 
            or response['status'] != Defines.STATUS_SUCCESS
        ):
            return False

        return True

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

        if self.getTrnref() == None or not Helper.isValidTrnRef(self.getTrnref()):
            raise IPC_Exception('Invalid TrnRef')

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
    * @return Refund
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self

    """
    * Transaction reference - transaction unique identifier
    *
    * @return string
    """
    def getTrnref(self):
        return self.__trnref

    """
    * Request identifier - must be unique
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID
