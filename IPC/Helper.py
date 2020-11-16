from IPC.Defines import Defines
import validators
import re
import html


class Helper(object):
    """
*  IPC Library helper functions
    """
    def __init__(_self):
        pass

    @staticmethod
    def isValidEmail(email: str):
        """
    *  Validate email address\n
    *  @param string email\n
    *  @return boolean
        """
        # if len(email) > 7:
        #  return bool(re.match(
        #      "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))
        return bool(validators.email(email))


    @staticmethod
    def isValidURL(url: str):
        """
    *  Validate URL address\n
    *  @param string url\n
    *  @return boolean
        """
        return bool(validators.url(url))


    @staticmethod
    def isValidIP(ip: str):
        """
    *  Validate IP address\n
    *  @param string ip\n
    *  @return boolean
        """
        return bool(validators.ipv4(ip))


    @staticmethod
    def isValidName(name: str):
        """
    *  Validate customer names\n
    *  @param string name\n
    *  @return boolean
        """
        return bool(re.match("^[a-zA-Z ]*", name))


    @staticmethod
    def isValidAmount(amt):
        """
    *  Validate amount.\n
    *  @param float amt\n
    *  @return boolean
        """
        return bool(re.match(r'^(-)?[0-9]+(?:\.[0-9]{0,2})?', str(amt)))


    @staticmethod
    def isValidCartQuantity(quantity):
        """
    *  Validate quantity\n
    *  @param int quantity\n
    *  @return boolean
        """
        return isinstance(quantity, int) and quantity > 0


    @staticmethod
    def isValidTrnRef(trnref):
        """
    *  Validate transaction reference\n
    *  @param string trnref\n
    *  @return boolean
        """
        #TODO
        return True


    @staticmethod
    def isValidOrderId(trnref):
        """
    *  Validate Order ID\n
    *  @param string trnref\n
    *  @return boolean
        """
        #TODO
        return True


    @staticmethod
    def isValidOutputFormat(outputFormat):
        """
    *  Validate output format\n
    *  @param string outputFormat\n
    *  @return boolean
        """
        return (outputFormat in [
            Defines.COMMUNICATION_FORMAT_XML,
            Defines.COMMUNICATION_FORMAT_JSON,
        ])


    @staticmethod
    def isValidCardNumber(cardNo: str):
        """
    *  Validate card number\n
    *  @param cardNo\n
    *  @return boolean
        """
        cardNo = cardNo.strip().replace(" ", "")
        if (not cardNo.isnumeric()) or (len(cardNo) > 19) or (len(cardNo) < 13):
            return False
        sum = dub = add = chk = 0
        even = 0
        for i in range(len(cardNo) - 1, -1, -1):
            if even == 1:
                dub = 2 * int(cardNo[i])
                if dub > 9:
                    add = dub - 9
                else:
                    add = dub
                even = 0
            else:
                add = cardNo[i]
                even = 1
            sum += add

        return ((sum % 10) == 0)


    @staticmethod
    def isValidCVC(cvc):
        """
    *  Validate card CVC\n
    *  @param cvc\n
    *  @return boolean
        """
        return (cvc.isnumeric() and len(cvc) == 3)

    @staticmethod
    def versionCheck(current, required):
        return int(current.replace('.', '')) >= int(required.replace('.', ''))


    @staticmethod
    def escape(text: str):
        """
    *  Escape HTML special chars\n
    *  @param string text\n
    *  @return string type
        """
        #('\'', '&#039;').replace('"', '&quot;') # ENT_QUOTES
        return html.escape(text)


    @staticmethod
    def unescape(text):
        """
    *  Unescape HTML special chars\n
    *  @param string text\n
    *  @return string
        """
        return html.unescape(text)


    @staticmethod
    def getArrayVal(array, key, default = '', notEmpty = False):
        """
    *  Return associative array element by key.
    *  If key not found in array returns default
    *  If notEmpty argument is TRUE returns default even if key is found in array but the element has empty value(0, None, '')\n
    *  @param array array
    *  @param mixed key
    *  @param string default
    *  @param bool notEmpty\n
    *  @return mixed
        """
        # TODO: select one of (list, dict)
        if not isinstance(array, (list, dict)):
            return default
        if notEmpty:
            if key in array:
                val = array[key].strip()
                if bool(val):
                    return val

            return default
        else:
            return array[key] if (key in array) else default


    @staticmethod
    def getValuesFromMultiDimensionalArray(array, values = []):
        """
    *  Returns one-dimensional array with all values from multi-dimensional array
    *  Useful when create request signature where only array values matter\n
    *  @param array array
    *  @param array values\n
    *  @return array
        """
        # TODO: select one of (list, dict)
        if not isinstance(array, (list, dict)):
            return values
        for k, v in array:
            # TODO: select one of (list, dict)
            if isinstance(v, (list, dict)):
                values = Helper.getValuesFromMultiDimensionalArray(v, values)
            else:
                values += v

        return values