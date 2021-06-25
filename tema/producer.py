"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import time
from threading import Thread

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs: a dict with the following format:
        {'name': <PRODUCER_ID>, 'daemon': True}
        The daemon argument always has the value True.
        A daemon thread runs without blocking the main program from exiting.
        And when main program exits, associated daemon threads are killed too.
        This is necessary because we want the producers to end their task
        when the consumers end their own task.
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.producer_id = marketplace.register_producer()
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time


    def run(self):
        """
        Over and over again,
        Producer sequentially produces the products specified in the input file
        with respect to quantity and waiting time to be realized(in seconds).
        So product info has the following format:
        [product_id, quantity, publish_wait_time].
        If the maximum quantity of the marketplace has been reached,
        we must wait some time( = no of seconds from republish_wait_time)
        and try again.
        """
        while True:
            # we parse every product
            for product_id, quantity, publish_wait_time in self.products:
                # we want to produce the product in the specified quantity
                curr_no = quantity
                while curr_no > 0:
                    will_be_published = self.marketplace.publish(self.producer_id, product_id)
                    # if we receive True, we decrement the current index and
                    # we wait for product to be published
                    if will_be_published:
                        curr_no -= 1
                        time.sleep(publish_wait_time)
                    # if we receive False, we should wait and try again after
                    else:
                        time.sleep(self.republish_wait_time)
