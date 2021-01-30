from selenium import webdriver
import re
import time
import random

datafile = open("testData.txt", "a")

class StreakBot():
    locationValue = []
    locationValue2 = []
    history = []
    automatedButton = None
    manualButton = None
    manualBetAmount = None
    startAutoBet = None
    manualAutoCashOut = None
    autoBetAmount = None
    cash = None
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.locationValue = []
        self.locationValue2 = []
        self.history = []
        self.automatedButton = None
        self.manualButton = None
        self.startAutoBet = None
        self.manualBetAmount = None
        self.manualAutoCashOut = None
        self.startManualBet = None
        self.autoBetAmount = None
        self.cash = None

    def login(self):
        self.driver.get('https://roobet.com/crash')
        time.sleep(3)
        self.locationValue = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]')
        self.locationValue2 = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]')
        self.automatedButton = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]')
        self.manualButton = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]')
        self.startAutoBet = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/button')
        self.manualBetAmount = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/input')
        self.manualAutoCashOut = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/input')
        self.startManualBet = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/button')
        self.autoBetAmount = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/input')

    def start(self):
        for _ in iter(int,1):
            self.tick()
            time.sleep(5)

    def tick(self):
        text = self.locationValue.text
        text = re.sub('[x]', '', text)
        text2 = self.locationValue2.text
        text2 = re.sub('[x]', '', text2)
        print(text)
        if not self.history:
            self.history.append(float(text))
            print("Adding " + text + "To history")
          
        elif float(text) != self.history[-1]: 
            self.history.append(float(text))
            datafile.write(str(text))
            datafile.write("\n")
            print("Adding " + text + "To history")
       

    def findStreak(self):
        biggestStreak = 0
        value = float(input("Enter limit value: "))
        currentStreak = 0
        inStreak = 0
        for element in self.history:  
            if inStreak == 1:
                if element >= value:
                    inStreak = 0
                    currentStreak = 0
                else:
                    currentStreak+=1
                    if currentStreak > 2:
                        print("Streak Greater than 2")
            elif element < value:
                inStreak = 1
                currentStreak = 1
            if currentStreak > biggestStreak:
                biggestStreak = currentStreak
        print(biggestStreak)
        print("The biggest Streak of values below " + str(value) + " was: " + str(biggestStreak))


    def createHistory(self):
        self.history = open("testData.txt").readlines()
        self.history = [word.strip() for word in self.history]
        self.history = [float(i) for i in self.history]

    def findAfterDouble(self):
        counter = 0
        inputValue = float(input("Enter limit value: "))
        PositionArray = [0] * 25
        for counter in range(0,len(self.history)):
            if self.history[counter] < inputValue:
                if counter + 1 < len(self.history):
                    if self.history[counter+1] < inputValue:
                        self.findPositions(PositionArray, counter + 1, inputValue)
        print("Position Array: ")
        print(PositionArray)

    def findPositions(self, PositionArray, startIndex, targetValue):
        for i in range(0,25):
            if(startIndex + i < len(self.history) and self.history[startIndex + i] < targetValue):
                PositionArray[i] += 1

    def automate(self):
        #betAmount = float(input("Enter Bet Amount: "))
        cashOut = float(input("Enter CashOut Value: "))
        #stopOnLoss = float(input("Enter stop on loss amount: "))
        #skipNo = int(input("Enter number of spaces to skip on 2 losses: "))

        
        self.startAutoBet.click()

        self.cash = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/header/div/div[1]/div/div[2]')
        cashValue = self.cash.text
        cashValue = re.sub('[$]', '', cashValue)
        cashValue = float(cashValue)
        initialCashValue = cashValue

        for _ in iter(int,1):
            text1 = self.locationValue.text
            text1 = re.sub('[x]', '', text1)
            text2 = self.locationValue2.text
            text2 = re.sub('[x]', '', text2)
            
            cashValue = self.cash.text
            cashValue = re.sub('[$]', '', cashValue)
            cashValue = float(cashValue)
            
            print("$" + str(cashValue))
        

            #and float(text2) < cashOut
            if float(text1) < 2.0:    
                print("Inside If Statement")          
                self.startAutoBet = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/button')
                self.startAutoBet.click()
                #wait until 2 rounds hav
                # e passed  
                self.wait(2)

                #Place the manual bets
                self.manualButton = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]')
                self.manualButton.click()
                
                self.manualBetAmount = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/input')
                self.manualBetAmount.clear()
                self.manualBetAmount.send_keys(self.getBetAmount(initialCashValue, 1))
                self.manualAutoCashOut.clear()
                self.manualAutoCashOut.send_keys("1.07")
                self.startManualBet.click()
               
                self.wait(1)
                
                curr = self.locationValue.text
                curr = re.sub('[x]', '', curr)
                if float(curr) < cashOut:  
                    self.manualButton = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]')
                    self.manualButton.click()    
                    self.manualBetAmount.clear()
                    self.manualBetAmount.send_keys(self.getBetAmount(initialCashValue, 2))
                    self.manualAutoCashOut.clear()
                    self.manualAutoCashOut.send_keys("1.07")
                    self.startManualBet.click()

                self.wait(1)


                self.automatedButton.click()
                
                cashValue = self.cash.text
                cashValue = re.sub('[$]', '', cashValue)
                cashValue = float(cashValue)
                
                self.autoBetAmount = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/input')
                self.autoBetAmount.clear()
                time.sleep(0.1)
                self.autoBetAmount.send_keys(self.getBetAmount(cashValue, 0))

                initialCashValue = cashValue
                time.sleep(0.1)

                self.startAutoBet.click()
                self.wait(1)
            
    
            time.sleep(3)

    def getBetAmount(self, CashAmount, currentLossStreak):
        Num = CashAmount - (0.06*CashAmount)
        initialDivisor = float(98.26/104.4)
        secondDivisor = float(0.34/5.78)
        betAmount = float(Num * initialDivisor)
        for counter in range(3-currentLossStreak):
            betAmount = betAmount * secondDivisor
            print(betAmount)
        return str(round(betAmount,4))


    def findInstances(self):
        inputValue = float(input("Enter value: "))
        counter = 0
        for element in self.history:
            if element < 1.1:
                counter+=1
        print(counter)

    def wait(self, turns):
        currentValue = None
        counter = -1
        for _ in iter(int, 1):
            if currentValue != self.locationValue.text:
                print("waited a turn")
                counter+=1
                currentValue = self.locationValue.text

            if counter == turns:
                break

            
bot = StreakBot()
time.sleep(3)
bot.login()



