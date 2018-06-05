import heapq
import csv
import random
import collections

class Order:
    def __init__(self, time, name, ticker, BorS, volume, price):
        self.time = time
        self.name = name
        self.ticker = ticker
        self.BorS = BorS
        self.volume = int(volume)
        self.price = int(price)

class miniOrder:
    def __init__(self):
        self.heapBuy = []
        self.heapSell = []
        self.mapOfPrices = {}

    def processOrder(self, order):
        if(order.BorS == "buy"):
            #If the HeapSell has no orders... Just add order to buy list
            if(len(heapq.nsmallest(1, self.heapSell)) == 0):
                self.addOrder(order)
            #If the Sell Heap, smallest price is smaller or equal order.price then fulfill Order
            elif(heapq.nsmallest(1, self.heapSell)[0] <= order.price):
                self.fulfillOrder(order,"buy")
            else:
                #Else, just add buy order to the buySide
                self.addOrder(order)
        if(order.BorS == "sell"):
            #If the buy side has nothing, just add order to sell side
            if(len(heapq.nlargest(1, self.heapBuy)) == 0):
                self.addOrder(order)
            #If the buy side is greater than or equal to selling price, fulfill the order
            elif(heapq.nlargest(1, self.heapBuy)[0] >= order.price):
                self.fulfillOrder(order,"sell")
            else: #Else just add order to the sell side
                self.addOrder(order)

    def fulfillOrder(self, order, transactionType):
        if(transactionType == "buy"):
            #Grab the Key from Sell Heap
            key = heapq.nsmallest(1, self.heapSell)[0]
            volumeAvaliable = self.mapOfPrices[key][0].volume
            if(order.volume > volumeAvaliable):
                print("Buying Order has been partially filled")
                order.volume -= volumeAvaliable
                self.mapOfPrices[key].popleft()
                if(len(self.mapOfPrices[key])==0):
                    heapq.heappop(self.heapSell)
                self.processOrder(order) #Reprocess to Check if there are more orders to fulfill
                print("Reprocessing")
            elif(order.volume < volumeAvaliable):
                print("Order has been fully fulfilled; Lowest Sell Order Partially Filled")
                self.mapOfPrices[key][0].volume -= order.volume
            else:
                print("Order and lowest sell Order has been fully filled")
                self.mapOfPrices[key].popleft()
                if(len(self.mapOfPrices[key]) == 0):
                    heapq.heappop(self.heapSell)
        else:
            if (transactionType == "sell"):
                # Grab the Key from Sell Heap
                key = heapq.nsmallest(1, self.heapBuy)[0]
                volumeAvaliable = self.mapOfPrices[key][0].volume
                if (order.volume > volumeAvaliable):
                    print("Selling Order has been partially filled")
                    order.volume -= volumeAvaliable
                    self.mapOfPrices[key].popleft()
                    if (len(self.mapOfPrices[key]) == 0):
                        heapq.heappop(self.heapBuy)
                    self.processOrder(order)  # Reprocess to Check if there are more orders to fulfill
                    print("Reprocessing")
                elif (order.volume < volumeAvaliable):
                    print("Selling Order has been fully fulfilled; Highest Buy Order Partially Filled")
                    self.mapOfPrices[key][0].volume -= order.volume
                else:
                    print("Order and highest Buy Order has been fully filled")
                    self.mapOfPrices[key].popleft()
                    if (len(self.mapOfPrices[key]) == 0):
                        heapq.heappop(self.heapBuy)

    def addOrder(self, order):
        #Pushes Onto the Heap the Price
        if(order.BorS == "buy"):
            if order.price not in self.mapOfPrices:
                heapq.heappush(self.heapBuy, order.price)
        else:
            if order.price not in self.mapOfPrices:
                heapq.heappush(self.heapSell, order.price)

        #Add to a map with Queues
        if order.price not in self.mapOfPrices:
            self.mapOfPrices[order.price] = collections.deque()
            self.mapOfPrices[order.price].append(order)
        elif order.price in self.mapOfPrices:
            self.mapOfPrices[order.price].append(order)

class tickerManager:
    def __init__(self):
        self.tickerKeys = {}
    def processOrder(self, order):
        if(order.ticker not in self.tickerKeys):
            #Create a Mini Order Book related to that Ticker
            self.tickerKeys[order.ticker] = miniOrder()
            self.tickerKeys[order.ticker].addOrder(order)
        else:
            self.tickerKeys[order.ticker].processOrder(order)

def init(fileName):
    orderBook = tickerManager()
    with open(fileName) as f:
        for line in f:
            lineList = line.split(",")
            tempOrder = Order(lineList[0], lineList[1], lineList[2], lineList[3], lineList[4], lineList[5])
            orderBook.processOrder(tempOrder)


init("m.csv")