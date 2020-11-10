from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCGetPaymentStatus.
 * Collect, validate and send API params
"""


class GetPaymentStatus(Base):
    __orderID: str

    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
    * Initiate API request
    *
    * @return Response
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCGetPaymentStatus')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

        self._addPostParam('OrderID', self.getOrderID())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    """
    * Validate all set details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getOrderID() == None or not Helper.isValidOrderId(self.getOrderID()):
            raise IPC_Exception('Invalid OrderId')

        if self.getOutputFormat() == None or not Helper.isValidOutputFormat(self.getOutputFormat()):
            raise IPC_Exception('Invalid Output format')

        return True

    """
    * Original request order id
    *
    * @return string
    """
    def getOrderID(self):
        return self.__orderID

    """
    * Original request order id
    *
    * @param string orderID
    *
    * @return self
    """
    def setOrderID(self, orderID: str):
        self.__orderID = orderID

        return self
