"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import time
from threading import Thread

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs: a dict with the following format:
        {'name': <CONSUMER_ID>}.
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        """
        Here we make orders for every cart of the consumer.
        """
        # we parse every cart of the consumer
        for cart in self.carts:
            # we create a new cart for the consumer
            cart_id = self.marketplace.new_cart()
            # we parse every action that is done with the current cart
            for action in cart:
                # we want to produce the action in the specified number of times
                curr_no = action["quantity"]
                while curr_no > 0:
                    # we verify the type of action
                    if action["type"] == "add":
                        is_added = self.marketplace.add_to_cart(cart_id, action["product"])
                        # if the product is successfully added to the cart,
                        # we decrease the current number
                        if is_added:
                            curr_no -= 1
                        # else, we should wait and try again after
                        else:
                            time.sleep(self.retry_wait_time)
                    # the action of removing is always successful
                    # so we don't have to verify anything,
                    # just decrease the current number after
                    elif action["type"] == "remove":
                        self.marketplace.remove_from_cart(cart_id, action["product"])
                        curr_no -= 1
            # now we can place the order for this cart
            self.marketplace.place_order(cart_id)
