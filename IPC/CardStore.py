import abc
from IPC.Base import Base
from IPC.IPC_Exception import IPC_Exception

class CardStore(Base, metaclass=abc.ABCMeta):
    CARD_VERIFICATION_NO = 1
    CARD_VERIFICATION_YES = 2
    __currency = 'EUR'
    __cardVerification: int
    __amount: float

    """
    * Amount of the transaction
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.
    *
    * @return float
    """
    def getAmount(self):
        return self.__amount

    """
    * Amount of the transaction.
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.
    *
    * @param float amount
    """
    def setAmount(self, amount: float):
        self.__amount = amount

    """
    * Specify whether the inputted card data to be verified or not before storing
    *
    * @param int cardVerification
    """
    def setCardVerification(self, cardVerification: int):
        self.__cardVerification = cardVerification

    """
    * Validate all set purchase details
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        if (self.getCardVerification() == None or (not self.getCardVerification() in [
                self.CARD_VERIFICATION_NO,
                self.CARD_VERIFICATION_YES,
            ])):
            raise IPC_Exception('Invalid card verification')

        if (self.getCardVerification()) == None:
            raise IPC_Exception('Invalid __currency')

        return True

    """
    * Specify whether the inputted card data to be verified or not before storing
    *
    * @return int
    """
    def getCardVerification(self):
        return self.__cardVerification

    """
    * ISO-4217 Three letter __currency code
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.
    *
    * @return string
    """
    def getCurrency(self):
        return self.__currency

    """
    * ISO-4217 Three letter __currency code
    * Used in the request if CardVerification = CARD_VERIFICATION_YES.
    *
    * @param string currency
    *
    * @return CardStore
    """
    def setCurrency(self, currency: str):
        self.__currency = currency

        return self
