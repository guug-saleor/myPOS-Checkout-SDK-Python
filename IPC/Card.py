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

    def getCardType(self):
        """
    *  @return int
        """
        return self.__cardType

    def setCardType(self, cardType: int):
        """
    * @param int cardType
        """
        self.__cardType = cardType

    def setCardNumber(self, cardNumber: str):
        """
    * @param string cardNumber
        """
        self.__cardNumber = cardNumber

    def getCardHolder(self):
        """
    * @return string
        """
        return self.__cardHolder

    def setCardHolder(self, cardHolder: str):
        """
    * @param string cardHolder
        """
        self.__cardHolder = cardHolder

    def setExpMM(self, expMM: str):
        """
    * @param string expMM
        """
        self.__expMM = expMM

    def setExpYY(self, expYY: str):
        """
    * @param string expYY
        """
        self.__expYY = expYY

    def setCvc(self, cvc ):
        """
    * @param string cvc 
        """
        self.__cvc  = cvc 

    def getEci(self):
        """
    * @return string
        """
        return self.__eci

    def setEci(self, eci: str):
        """
    * @param string eci
        """
        self.__eci = eci

    def getAvv(self):
        """
    * @return string
        """
        return self.__avv

    def setAvv(self, avv: str):
        """
    * @param string avv
        """
        self.__avv = avv

    def getXid(self):
        """
    * @return string
        """
        return self.__xid

    def setXid(self, xid: str):
        """
    * @param string xid
        """
        self.__xid = xid

    def setCardToken(self, cardToken: str):
        """
    * @param string cardToken
        """
        self.__cardToken = cardToken

    def validate(self):
        """
    * @return bool
    * @raises IPC_Exception
        """
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

    def getCardToken(self):
        """
    * @return string
        """
        return self.__cardToken

    def getCardNumber(self):
        """
    * @return string
        """
        return self.__cardNumber

    def getCvc(self):
        """
    * @return string
        """
        return self.__cvc 

    def getExpMM(self):
        """
    * @return string
        """
        return self.__expMM

    def getExpYY(self):
        """
    * @return string
        """
        return self.__expYY

    def getExpDate(self):
        """
    * Date in format YYMM\n
    * @return string
        """
        return self.getExpYY().ljust(2) + self.getExpMM().ljust(2)
