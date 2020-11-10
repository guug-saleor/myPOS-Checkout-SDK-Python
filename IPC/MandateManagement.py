from IPC.Base import Base
from IPC.Config import Config
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCMandateManagement.
 * Collect, validate and send API params
"""
class MandateManagement(Base):
    MANDATE_MANAGEMENT_ACTION_REGISTER = 1
    MANDATE_MANAGEMENT_ACTION_CANCEL = 2
    __mandateReference: str
    __customerWalletNumber: str
    __action: int
    __mandateText: str

    """
    * Return Refund object
    *
    * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
    * Identifier of the client’s (debtor’s) myPOS account
    *
    * @param string customerWalletNumber
    """
    def setCustomerWalletNumber(self, customerWalletNumber: str):
        self.__customerWalletNumber = customerWalletNumber

    """
    * Registration / Cancellation of a MandateReference
    *
    * @param int action
    """
    def setAction(self, action: int):
        self.__action = action

    """
    * Text supplied from the merchant, so the client can easily identify the Mandate.
    *
    * @param string mandateText
    """
    def setMandateText(self, mandateText: str):
        self.__mandateText = mandateText

    """
    * Initiate API request
    *
    * @return Response
    * @raises IPC_Exception
    """
    def process(self):
        self.validate()
        self._addPostParam('IPCmethod', 'IPCMandateManagement')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())
        self._addPostParam('MandateReference', self.getMandateReference())
        self._addPostParam('CustomerWalletNumber', self.getCustomerWalletNumber())
        self._addPostParam('Action', self.getAction())
        self._addPostParam('MandateText', self.getMandateText())
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

        if self.getOutputFormat() == None or not Helper.isValidOutputFormat(self.getOutputFormat()):
            raise IPC_Exception('Invalid Output format')

        return True

    """
    * Unique identifier of the agreement (mandate) between the merchant and the client (debtor). Up to 127 characters.
    *
    * @return string
    """
    def getMandateReference(self):
        return self.__mandateReference

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
    * @return string
    """
    def getCustomerWalletNumber(self):
        return self.__customerWalletNumber

    """
    * Registration / Cancellation of a MandateReference
    *
    * @return int
    """
    def getAction(self):
        return self.__action

    """
    * Text supplied from the merchant, so the client can easily identify the Mandate.
    *
    * @return string
    """
    def getMandateText(self):
        return self.__mandateText
