from IPC.Helper import Helper
from IPC.IPC_Exception import IPC_Exception


"""
 * Purchase cart object
"""
class Cart(object):
    ITEM_TYPE_ARTICLE = 'article'
    ITEM_TYPE_DELIVERY = 'delivery'
    ITEM_TYPE_DISCOUNT = 'discount'

    """
    * Array containing cart items
    *
    * @var array
    """
    __cart = []

    """
    *
    * @param string itemName Item name
    * @param int quantity Items quantity
    * @param float price Single item price
    *
    * @param string type
    * @return Cart
    * @raises IPC_Exception
    """
    def add(self, itemName, quantity, price, type = ITEM_TYPE_ARTICLE):
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

    """
    * Returns cart total amount
    *
    * @return float
    """
    def getTotal(self):
        sum = 0
        if bool(self.__cart):
            for v in self.__cart :
                sum += v['quantity'] * v['price']

        return sum

    """
    * Returns count of items in cart
    *
    * @return int
    """
    def getItemsCount(self):
        # TODO: select one of (list, tuple)
        return self.__cart.count if (bool(self.__cart) and isinstance(self.__cart, (list, tuple))) else 0

    """
    * Validate cart items
    *
    * @return boolean
    * @raises IPC_Exception
    """
    def validate(self):
        if not self.getCart() or self.getItemsCount() == 0:
            raise IPC_Exception('Missing cart items')

        return True

    """
    * Return cart array
    *
    * @return array
    """
    def getCart(self):
        return self.__cart
