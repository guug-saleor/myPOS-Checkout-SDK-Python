from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class GetPaymentStatus(Base):
    """
 * Process IPC method: IPCGetPaymentStatus.
 * Collect, validate and send API params
    """
    __orderID: str

    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    def process(self):
        """
    * Initiate API request\n
    * @return Response
    * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCGetPaymentStatus')
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
    * Validate all set details\n
    * @return boolean
    * @raises IPC_Exception
        """
        try:
            self._getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getOrderID() == None or not Helper.isValidOrderId(self.getOrderID()):
            raise IPC_Exception('Invalid OrderId')

        if self.getOutputFormat() == None or not Helper.isValidOutputFormat(self.getOutputFormat()):
            raise IPC_Exception('Invalid Output format')

        return True

    def getOrderID(self):
        """
    * Original request order id\n
    * @return string
        """
        return self.__orderID

    def setOrderID(self, orderID: str):
        """
    * Original request order id\n
    * @param string orderID\n
    * @return self
        """
        self.__orderID = orderID

        return self
