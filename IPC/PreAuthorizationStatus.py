from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class PreAuthorizationStatus(Base):
    """
 * Process IPC method: IPCPreAuthorizationStatus.
 * Collect, validate and send API params
    """
    __orderID: str

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
    * @return PreAuthorizationStatus
        """
        self.__orderID = orderID

        return self

    def process(self):
        """
    * Initiate API request\n
    * @return Response
    * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCPreAuthStatus')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

        self._addPostParam('OrderID', self.getOrderID())

        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    def validate(self):
        """
    * Validate all set purchase details\n
    * @return boolean
    * @raises IPC_Exception
        """
        try:
            self._getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if not Helper.versionCheck(self._getCnf().getVersion(), '1.4'):
            raise IPC_Exception('IPCVersion ' + self._getCnf().getVersion() + ' does not support IPCPreAuthorizationStatus method. Please use 1.4 or above.')

        return True

    def getOrderID(self):
        """
    * Purchase identifier\n
    * @return string
        """
        return self.__orderID
