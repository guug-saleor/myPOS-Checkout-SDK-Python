import datetime
from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class Card(object):
    CARD_TYPE_MASTERCARD = 1
    CARD_TYPE_MAESTRO = 2
    CARD_TYPE_VISA = 3
    CARD_TYPE_VISA_ELECTRON = 4
    CARD_TYPE_VPAY = 5
    CARD_TYPE_JCB = 6

    __cardType: int
    __cardNumber: str
    __cardHolder: str
    __expMM: str
    __expYY: str
    __cvc: str
    __eci: str
    __avv: str
    __xid: str
    __cardToken: str

    """
    *  @return int
    """
    def getCardType(self):
        return self.__cardType

    """
    * @param int cardType
    """
    def setCardType(self, cardType: int):
        self.__cardType = cardType

    """
    * @param string cardNumber
    """
    def setCardNumber(self, cardNumber: str):
        self.__cardNumber = cardNumber

    """
    * @return string
    """
    def getCardHolder(self):
        return self.__cardHolder

    """
    * @param string cardHolder
    """
    def setCardHolder(self, cardHolder: str):
        self.__cardHolder = cardHolder

    """
    * @param string expMM
    """
    def setExpMM(self, expMM: str):
        self.__expMM = expMM

    """
    * @param string expYY
    """
    def setExpYY(self, expYY: str):
        self.__expYY = expYY

    """
    * @param string cvc 
    """
    def setCvc(self, cvc ):
        self.__cvc  = cvc 

    """
    * @return string
    """
    def getEci(self):
        return self.__eci

    """
    * @param string eci
    """
    def setEci(self, eci: str):
        self.__eci = eci

    """
    * @return string
    """
    def getAvv(self):
        return self.__avv

    """
    * @param string avv
    """
    def setAvv(self, avv: str):
        self.__avv = avv

    """
    * @return string
    """
    def getXid(self):
        return self.__xid

    """
    * @param string xid
    """
    def setXid(self, xid: str):
        self.__xid = xid

    """
    * @param string cardToken
    """
    def setCardToken(self, cardToken: str):
        self.__cardToken = cardToken

    """
    * @return bool
    * @raises IPC_Exception
    """
    def validate(self):
        if self.getCardToken():
            return True

        if self.getCardNumber() == None or not Helper.isValidCardNumber(self.getCardNumber()):
            raise IPC_Exception('Invalid card number')

        if self.getCvc() == None or not Helper.isValidCVC(self.getCvc()):
            raise IPC_Exception('Invalid card CVC')

        if self.getExpMM() == None or not self.getExpMM().isnumeric() or int(self.getExpMM() or "") <= 0 or int(self.getExpMM() or "") > 12:
            raise IPC_Exception('Invalid card expire date (MM)')

        if self.getExpYY() == None or not self.getExpYY().isnumeric() or int(self.getExpYY() or "") < datetime.datetime.today().year:
            raise IPC_Exception('Invalid card expire date (YY)')

        return False

    """
    * @return string
    """
    def getCardToken(self):
        return self.__cardToken

    """
    * @return string
    """
    def getCardNumber(self):
        return self.__cardNumber

    """
    * @return string
    """
    def getCvc(self):
        return self.__cvc 

    """
    * @return string
    """
    def getExpMM(self):
        return self.__expMM

    """
    * @return string
    """
    def getExpYY(self):
        return self.__expYY

    """
    * Date in format YYMM
    *
    * @return string
    """
    def getExpDate(self):
        return self.getExpYY().ljust(2) + self.getExpMM().ljust(2)
