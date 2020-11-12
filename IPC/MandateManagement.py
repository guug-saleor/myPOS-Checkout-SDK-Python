from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class MandateManagement(Base):
    """
 * Process IPC method: IPCMandateManagement.
 * Collect, validate and send API params
    """
    MANDATE_MANAGEMENT_ACTION_REGISTER = 1
    MANDATE_MANAGEMENT_ACTION_CANCEL = 2
    __mandateReference: str
    __customerWalletNumber: str
    __action: int
    __mandateText: str

    def __init__(self, cnf: Config):
        """
    * Return Refund object\n
    * @param cnf: Config
        """
        self._setCnf(cnf)

    def setCustomerWalletNumber(self, customerWalletNumber: str):
        """
    * Identifier of the client’s (debtor’s) myPOS account\n
    * @param string customerWalletNumber
        """
        self.__customerWalletNumber = customerWalletNumber

    def setAction(self, action: int):
        """
    * Registration / Cancellation of a MandateReference\n
    * @param int action
        """
        self.__action = action

    def setMandateText(self, mandateText: str):
        """
    * Text supplied from the merchant, so the client can easily identify the Mandate.\n
    * @param string mandateText
        """
        self.__mandateText = mandateText

    def process(self):
        """
    * Initiate API request\n
    * @return Response
    * @raises IPC_Exception
        """
        self.validate()
        self._addPostParam('IPCmethod', 'IPCMandateManagement')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())
        self._addPostParam('MandateReference', self.getMandateReference())
        self._addPostParam('CustomerWalletNumber', self.getCustomerWalletNumber())
        self._addPostParam('Action', self.getAction())
        self._addPostParam('MandateText', self.getMandateText())
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

        if self.getOutputFormat() == None or not Helper.isValidOutputFormat(self.getOutputFormat()):
            raise IPC_Exception('Invalid Output format')

        return True

    def getMandateReference(self):
        """
    * Unique identifier of the agreement (mandate) between the merchant and the client (debtor). Up to 127 characters.\n
    * @return string
        """
        return self.__mandateReference

    def setMandateReference(self, mandateReference: str):
        """
    * Unique identifier of the agreement (mandate) between the merchant and the client (debtor). Up to 127 characters.\n
    * @param string mandateReference
        """
        self.__mandateReference = mandateReference

    def getCustomerWalletNumber(self):
        """
    * Identifier of the client’s (debtor’s) myPOS account\n
    * @return string
        """
        return self.__customerWalletNumber

    def getAction(self):
        """
    * Registration / Cancellation of a MandateReference\n
    * @return int
        """
        return self.__action

    def getMandateText(self):
        """
    * Text supplied from the merchant, so the client can easily identify the Mandate.\n
    * @return string
        """
        return self.__mandateText
