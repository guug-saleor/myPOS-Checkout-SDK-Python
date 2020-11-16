from IPC.Config import Config
from IPC.Base import Base
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class Reversal(Base):
    """
 * Process IPC method: IPCReversal.
 * Collect, validate and send API params
    """
    __trnref: str

    def __init__(self, cnf: Config):
        """
     * Return Refund object

     * @param cnf: Config
        """
        self._setCnf(cnf)

    def process(self):
        """
     * Initiate API request

     * @return Response
     * @raises IPC_Exception
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCReversal')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())
        self._addPostParam('IPC_Trnref', self.getTrnref())
        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    def validate(self):
        """
     * Validate all set refund details

     * @return boolean
     * @raises IPC_Exception
        """
        try:
            self._getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getTrnref() == None or not Helper.isValidTrnRef(self.getTrnref()):
            raise IPC_Exception('Invalid TrnRef')

        if self.getOutputFormat() == None or not Helper.isValidOutputFormat(self.getOutputFormat()):
            raise IPC_Exception('Invalid Output format')

        return True

    def getTrnref(self):
        """
     * Transaction reference - transaction unique identifier

     * @return string
        """
        return self.__trnref

    def setTrnref(self, trnref: str):
        """
     * Transaction reference - transaction unique identifier

     * @param string trnref

     * @return Reversal
        """
        self.__trnref = trnref

        return self
