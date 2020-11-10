from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception
from IPC.Purchase import Purchase


"""
 * Customer details class.
 * Collect and validate client details
"""
class Customer(object):
    __email: str
    __phone: str
    __firstName: str
    __lastName: str
    __country: str
    __city: str
    __zip: str
    __address: str

    """
    * Customer Phone number
    *
    * @return string
    """
    def getPhone(self):
        return self.__phone

    """
    * Customer Phone number
    *
    * @param string phone
    *
    * @return Customer
    """
    def setPhone(self, phone: str):
        self.__phone = phone

        return self

    """
    * Customer country code ISO 3166-1
    *
    * @return string
    """
    def getCountry(self):
        return self.__country

    """
    * Customer country code ISO 3166-1
    *
    * @param string country
    *
    * @return Customer
    """
    def setCountry(self, country: str):
        self.__country = country

        return self

    """
    * Customer city
    *
    * @return string
    """
    def getCity(self):
        return self.__city

    """
    * Customer city
    *
    * @param string city
    *
    * @return Customer
    """
    def setCity(self, city: str):
        self.__city = city

        return self

    """
    * Customer ZIP code
    *
    * @return string
    """
    def getZip(self):
        return self.__zip

    """
    * Customer ZIP code
    *
    * @param string zip
    *
    * @return Customer
    """
    def setZip(self, zip: str):
        self.__zip = zip

        return self

    """
    * Customer address
    *
    * @return string
    """
    def getAddress(self):
        return self.__address

    """
    * Customer address
    *
    * @param string address
    *
    * @return Customer
    """
    def setAddress(self, address: str):
        self.__address = address

        return self

    """
    * Validate all set customer details
    *
    * @param string paymentParametersRequired
    *
    * @return bool
    * @raises IPC_Exception
    """
    def validate(self, paymentParametersRequired):
        if paymentParametersRequired == Purchase.PURCHASE_TYPE_FULL:

            if self.getFirstName() == None:
                raise IPC_Exception('Invalid First name')

            if self.getLastName() == None:
                raise IPC_Exception('Invalid Last name')

            if self.getEmail() == None or not Helper.isValidEmail(self.getEmail()):
                raise IPC_Exception('Invalid Email')

        return True

    """
    * Customer first name
    *
    * @return string
    """
    def getFirstName(self):
        return self.__firstName

    """
    * Customer first name
    *
    * @param string firstName
    *
    * @return Customer
    """
    def setFirstName(self, firstName: str):
        self.__firstName = firstName

        return self

    """
    * Customer last name
    *
    * @return string
    """
    def getLastName(self):
        return self.__lastName

    """
    * Customer last name
    *
    * @param string lastName
    *
    * @return Customer
    """
    def setLastName(self, lastName: str):
        self.__lastName = lastName

        return self

    """
    * Customer Email address
    *
    * @return string
    """
    def getEmail(self):
        return self.__email

    """
    * Customer Email address
    *
    * @param string email
    *
    * @return Customer
    """
    def setEmail(self, email: str):
        self.__email = email

        return self
