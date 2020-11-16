import abc
from IPC.Base import Base
from IPC.IPC_Exception import IPC_Exception

class CardStore(Base, metaclass=abc.ABCMeta):
    CARD_VERIFICATION_NO = 1
    CARD_VERIFICATION_YES = 2
    __currency = 'EUR'
    __cardVerification: int
    __amount: float

    def getAmount(self):
        """
    * Amount of the transaction
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.\n
    * @return float
        """
        return self.__amount

    def setAmount(self, amount: float):
        """
    * Amount of the transaction.
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.\n
    * @param float amount
        """
        self.__amount = amount

    def setCardVerification(self, cardVerification: int):
        """
    * Specify whether the inputted card data to be verified or not before storing\n
    * @param int cardVerification
        """
        self.__cardVerification = cardVerification

    def validate(self):
        """
    * Validate all set purchase details\n
    * @return boolean
    * @raises IPC_Exception
        """
        if (self.getCardVerification() == None or (not self.getCardVerification() in [
                self.CARD_VERIFICATION_NO,
                self.CARD_VERIFICATION_YES,
            ])):
            raise IPC_Exception('Invalid card verification')

        if (self.getCardVerification()) == None:
            raise IPC_Exception('Invalid currency')

        return True

    def getCardVerification(self):
        """
    * Specify whether the inputted card data to be verified or not before storing\n
    * @return int
        """
        return self.__cardVerification

    def getCurrency(self):
        """
    * ISO-4217 Three letter currency code
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.\n
    * @return string
        """
        return self.__currency

    def setCurrency(self, currency: str):
        """
    * ISO-4217 Three letter currency code
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.\n
    * @param string currency\n
    * @return CardStore
        """
        self.__currency = currency

        return self
