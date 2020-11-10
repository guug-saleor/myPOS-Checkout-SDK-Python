from IPC.Card import Card
from IPC.CardStore import CardStore
from IPC.Config import Config
from IPC.IPC_Exception import IPC_Exception


"""
 * Process IPC method: IPCIAStoreCard.
 * Collect, validate and send API params
"""
class IAStoredCardUpdate(CardStore):
    """
    * @var Card
    """
    __card: Card

    """
    * Return purchase object
    *
    * @param cnf: Config
    """
    def __init__(self, cnf: Config):
        self._setCnf(cnf)

    """
    * Initiate API request
    *
    * @return Response
    """
    def process(self):
        self.validate()

        self._addPostParam('IPCmethod', 'IPCIAStoredCardUpdate')
        self._addPostParam('IPCVersion', self.getCnf().getVersion())
        self._addPostParam('IPCLanguage', self.getCnf().getLang())
        self._addPostParam('SID', self.getCnf().getSid())
        self._addPostParam('WalletNumber', self.getCnf().getWallet())
        self._addPostParam('KeyIndex', self.getCnf().getKeyIndex())
        self._addPostParam('Source', self.getCnf().getSource())

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

    """
    * Validate all set purchase details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        super().validate()

        try:
            self.getCnf().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Config details: {ex}')

        if self.getCard() == None:
            raise IPC_Exception('Missing card details')

        try:
            self.getCard().validate()
        except Exception as ex:
            raise IPC_Exception(f'Invalid Card details: {ex}')

        return True

    """
    * Card object
    *
    * @return Card
    """
    def getCard(self):
        return self.__card

    """
    * Card object
    *
    * @param Card card
    """
    def setCard(self, card: Card):
        self.__card = card
