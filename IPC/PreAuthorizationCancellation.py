from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCPreAuthorizationCancellation.
 * Collect, validate and send API params
"""
class PreAuthorizationCancellation(Base):
    __currency = 'EUR'
    __amount: float
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
    * @return PreAuthorizationCancellation
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self

    """
    * ISO-4217 Three letter __currency code
    *
    * @param string currency
    *
    * @return PreAuthorizationCancellation
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self

    """
    *  The amount for completion
    * 
    * @param mixed amount
    *
    * @return PreAuthorizationCancellation
    """
    def setAmount(self, amount: float):
        self.__amount = amount

        return self

    """
    * Initiate API request
    *
    * @return Response
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCPreAuthCancellation')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('OrderID', self.getOrderID())

        self._addPostParam('Amount', self.getAmount())
        self._addPostParam('Currency', self.getCurrency())
        
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    """
    * Validate all set purchase details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if not Helper.versionCheck(self.getCnf().getVersion(), '1.4'):
            raise IPC_Exception('IPCVersion ' + self.getCnf().getVersion() + ' does not support IPCPreAuthorizationCancellation method. Please use 1.4 or above.')

        if self.getCurrency() == None:
            raise IPC_Exception('Invalid __currency')

        if self.getAmount() == None or not Helper.isValidAmount(self.getAmount()):
            raise IPC_Exception('Empty or invalid amount')
        
        return True

    """
    * ISO-4217 Three letter __currency code
    *
    * @return string
    """
    def getCurrency(self):
        return self.__currency

    """
    * Purchase identifier
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID
    
    """
    *  The amount for completion
    *
    * @return mixed
    """
    def getAmount(self):
        return self.__amount
    
