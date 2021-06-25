"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from collections import deque
from threading import currentThread, Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor.

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        # this lock is used when we register a producer
        self.register_producer_lock = Lock()
        # this dictionary has producer ids as keys
        # and products of producers(stores as deques) as values
        self.producers_queues = {}
        # this dictionary has products as keys and producer ids as values
        # it is used when a consumer remove the product from the cart
        # and we have to add it back to the initial producer queue
        self.product_producer = {}
        # this lock is used when we add a new cart
        self.new_cart_lock = Lock()
        # this dictionary has cart ids as keys and cart products as values
        self.cart_products = {}

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # we use lock to assign a new id and a new queue to the new producer
        # in an atomic way
        self.register_producer_lock.acquire()

        # we use the number of keys as the id for the new producer
        # which certainly hasn't been assigned to another one
        new_id = len(self.producers_queues)
        # we create a new deque that will contain products
        # of the new producer
        self.producers_queues[new_id] = deque()

        self.register_producer_lock.release()

        # we return the id for the new producer
        return new_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: Int
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # if the queue of the producer is not full:
        if len(self.producers_queues[producer_id]) < self.queue_size_per_producer:
            # we add the product in the queue
            self.producers_queues[producer_id].appendleft(product)
            # we add an entry with the product and the producer id
            self.product_producer[product] = producer_id
            # the product was added, so we return True
            return True
        # we cannot add the product, so we return False
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        # we use lock to assign a new id and a new queue to the new cart
        # in an atomic way
        self.new_cart_lock.acquire()

        # we use the number of keys as the id for the new cart
        # which certainly hasn't been assigned to another one
        cart_id = len(self.cart_products)
        # we create a new deque with products for the new cart
        self.cart_products[cart_id] = deque()

        self.new_cart_lock.release()

        # we return the id for the new cart
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        # we have to find if the product is in a producer queue
        # and remove it from the queue and add it to the cart
        # we return True if the product exists, otherwise False
        # all operations are thread-safe
        for producer_id in self.producers_queues:
            if product in self.producers_queues[producer_id]:
                self.producers_queues[producer_id].remove(product)
                self.cart_products[cart_id].appendleft(product)
                return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # we remove the product from cart and add it back to the producer queue
        # all operations are thread-safe
        self.cart_products[cart_id].remove(product)
        self.producers_queues[self.product_producer[product]].appendleft(product)

    def place_order(self, cart_id):
        """
        Return a deque with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # we obtain the deque with all the products from the cart
        products = self.cart_products[cart_id]

        # we parse every product that the customer bought and print it
        for product in products:
            # with the concatenation operator, print is atomic
            print(currentThread().getName() + " bought " + str(product))

        # we make the cart empty
        self.cart_products[cart_id] = None

        return products
