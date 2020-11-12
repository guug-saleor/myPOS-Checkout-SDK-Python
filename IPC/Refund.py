from IPC.Base import Base
from IPC.Config import Config
from IPC.Defines import Defines
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class Refund(Base):
    """
 * Process IPC method: IPCRefund.
 * Collect, validate and send API params
    """
    __currency = 'EUR'
    __orderID: str
    __trnref = None
    __amount: float

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

    def setTrnref(self, trnref: str):
        """
    * Transaction reference - transaction unique identifier\n
    * @param string trnref\n
    * @return Refund
        """
        self.__trnref = trnref

        return self

    def setOrderID(self, orderID: str):
        """
    * Request identifier - must be unique\n
    * @param string orderID\n
    * @return Refund
        """
        self.__orderID = orderID

        return self

    def process(self):
        """
    * Initiate API request\n
    * @return boolean
    * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCRefund')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

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

        if self.getTrnref() == None or not Helper.isValidTrnRef(self.getTrnref()):
            raise IPC_Exception('Invalid TrnRef')

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
    * ISO-4217 Three letter __currency code\n
    * @return string
        """
        return self.__currency

    def setCurrency(self, currency: str):
        """
    * ISO-4217 Three letter __currency code\n
    * @param string currency\n
    * @return Refund
        """
        self.__currency = currency

        return self

    def getTrnref(self):
        """
    * Transaction reference - transaction unique identifier\n
    * @return string
        """
        return self.__trnref

    def getOrderID(self):
        """
    * Request identifier - must be unique\n
    * @return string
        """
        return self.__orderID
