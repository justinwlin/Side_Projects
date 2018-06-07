import heapq
import csv
import random
import collections

#Order
class Order:
    def __init__(self, time, name, ticker, BorS, volume, price):
        self.time = time
        self.name = name
        self.ticker = ticker
        self.BorS = BorS
        self.volume = int(volume)
        self.price = int(price)

class OrderBook:
    def __init__(self):
        self.heapBuy = [] #Keep track of Buy Keys
        self.heapSell = [] #Keep Track of Sell Keys
        self.mapOfPrices = {} #Range of Prices

    #Process Order: Decides whether the order gets fulfilled or simply added to the buy/sell side
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

    #Logic to Match Orders
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
                #Basically if there are two separate orders with the same price, once the first one is popped in queue, reprocess to check.
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

    #Adds Orders to heap/map if orders can't be fulfilled
    def addOrder(self, order):
        #Pushes Onto the Heap the Price
        if(order.BorS == "buy"):
            #Make sure that the heap doesn't have two of the same key
            if order.price not in self.mapOfPrices: 
                heapq.heappush(self.heapBuy, order.price)
        else:
            if order.price not in self.mapOfPrices:
                heapq.heappush(self.heapSell, order.price)

        #Add to a map to keep track of prices and orders
        if order.price not in self.mapOfPrices:
            self.mapOfPrices[order.price] = collections.deque()
            self.mapOfPrices[order.price].append(order)
        elif order.price in self.mapOfPrices:
            self.mapOfPrices[order.price].append(order)

#Helps create a separation for all the different Ticket Prices
class tickerManager:
    def __init__(self):
        self.tickerKeys = {}
    def processOrder(self, order):
        if(order.ticker not in self.tickerKeys):
            #Create a Mini Order Book related to that Ticker
            self.tickerKeys[order.ticker] = OrderBook()
            self.tickerKeys[order.ticker].addOrder(order)
        else:
            self.tickerKeys[order.ticker].processOrder(order)

#Inits the File
def init(fileName):
    tickerM = tickerManager()
    control = True
    #Reading Through CSV File
    with open(fileName) as f:
        for line in f:
            lineList = line.split(",")
            tempOrder = Order(lineList[0], lineList[1], lineList[2], lineList[3], lineList[4], lineList[5])
            tickerM.processOrder(tempOrder)

    #User Input Loop
    while(control):
        print("Would you like to place an order?")
        print("Format: Time, name, ticker, buy/sell, volume, price")
        userInput = input()
        userInput = userInput.replace(" ", "")
        if(userInput == "quit"):
            break

        lineList = userInput.split(",")
        tempOrder = Order(lineList[0], lineList[1], lineList[2], lineList[3], lineList[4], lineList[5])
        tickerM.processOrder(tempOrder)



init("m.csv")