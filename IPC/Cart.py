from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


class Cart(object):
    """
 * Purchase cart object
    """
    ITEM_TYPE_ARTICLE = 'article'
    ITEM_TYPE_DELIVERY = 'delivery'
    ITEM_TYPE_DISCOUNT = 'discount'

    """
    * Array containing cart items\n
    * @var array
    """
    __cart = []

    def add(self, itemName, quantity, price, type = ITEM_TYPE_ARTICLE):
        """
    * @param string itemName Item name
    * @param int quantity Items quantity
    * @param float price Single item price
    * @param string type\n
    * @return Cart
    * @raises IPC_Exception
        """
        if not bool(itemName):
            raise IPC_Exception('Invalid cart item name')

        if not bool(quantity) or not Helper.isValidCartQuantity(quantity):
            raise IPC_Exception('Invalid cart item quantity')

        if not bool(price) or not Helper.isValidAmount(price):
            raise IPC_Exception('Invalid cart item price')

        item = {
            'name': itemName,
            'quantity': quantity,
            'price': price,
        }

        if type == self.ITEM_TYPE_DELIVERY:
            item['delivery'] = 1
        elif type == self.ITEM_TYPE_DISCOUNT:
            item['price'] = num = -1 * abs(item['price'])

        self.__cart += item

        return self

    def getTotal(self):
        """
    * Returns cart total amount\n
    * @return float
        """
        sum = 0
        if bool(self.__cart):
            for v in self.__cart :
                sum += v['quantity'] * v['price']

        return sum

    def getItemsCount(self):
        """
    * Returns count of items in cart\n
    * @return int
        """
        # TODO: select one of (list, dict)
        return self.__cart.count if (bool(self.__cart) and isinstance(self.__cart, (list, dict))) else 0

    def validate(self):
        """
    * Validate cart items\n
    * @return boolean
    * @raises IPC_Exception
        """
        if not self.getCart() or self.getItemsCount() == 0:
            raise IPC_Exception('Missing cart items')

        return True

    def getCart(self):
        """
    * Return cart array\n
    * @return array
        """
        return self.__cart
