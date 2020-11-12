from IPC.Card import Card
from IPC.CardStore import CardStore
from IPC.Config import Config
from IPC.IPC_Exception import IPC_Exception


class IAStoredCardUpdate(CardStore):
    """
 * Process IPC method: IPCIAStoreCard.
 * Collect, validate and send API params
    """

    __card: Card

    def __init__(self, cnf: Config):
        """
    * Return purchase object\n
    * @param cnf: Config
        """
        self._setCnf(cnf)

    def process(self):
        """
    * Initiate API request\n
    * @return Response
        """
        self.validate()

        self._addPostParam('IPCmethod', 'IPCIAStoredCardUpdate')
        self._addPostParam('IPCVersion', self._getCnf().getVersion())
        self._addPostParam('IPCLanguage', self._getCnf().getLang())
        self._addPostParam('SID', self._getCnf().getSid())
        self._addPostParam('WalletNumber', self._getCnf().getWallet())
        self._addPostParam('KeyIndex', self._getCnf().getKeyIndex())
        self._addPostParam('Source', self._getCnf().getSource())

        self._addPostParam('CardVerification', self.getCardVerification())
        if (self.getCardVerification()) == self.CARD_VERIFICATION_YES:
            self._addPostParam('Amount', self.getAmount())
            self._addPostParam('Currency', self.getCurrency())

        self._addPostParam('CardType', self.getCard().getCardType())
        self._addPostParam('CardToken', self.getCard().getCardToken())
        self._addPostParam('CardholderName', self.getCard().getCardHolder())
        self._addPostParam('ExpDate', self.getCard().getExpDate(), True)
        self._addPostParam('CVC', self.getCard().getCvc(), True)
        self._addPostParam('ECI', self.getCard().getEci())
        self._addPostParam('AVV', self.getCard().getAvv())
        self._addPostParam('XID', self.getCard().getXid())

        self._addPostParam('OutputFormat', self.getOutputFormat())

        return self._processPost()

    def validate(self):
        """
    * Validate all set purchase details\n
    * @return boolean
    * @raises IPC_Exception
        """
        super().validate()

        try:
            self._getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getCard() == None:
            raise IPC_Exception('Missing card details')

        try:
            self.getCard().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Card details: {ex}')

        return True

    def getCard(self):
        """
    * Card object\n
    * @return Card
        """
        return self.__card

    def setCard(self, card: Card):
        """
    * Card object\n
    * @param Card card
        """
        self.__card = card
