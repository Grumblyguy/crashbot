import random

class DoubleBot():
    def __init__(self, Balance, Cashout, NumLives, Multiplier):
        self.bal = Balance
        self.cashOut = Cashout
        self.NumLives = NumLives
        self.Multiplier = Multiplier
        self.bigBetState = 0
        self.Bots = []
        self.hasDoubled = 0
        self.numGames = 0
        self.failed = 0
    
    def runFinite(self, crashScore):
        if self.hasDoubled == 1 or self.failed == 1:
            return

        if self.Bots == []:
            self.Bots.append(Bot(100, self.cashOut, self.NumLives, self.Multiplier))
        self.numGames+=1
        self.Bots[-1].runFinite(crashScore)

        if self.Bots[-1].failed == 1 and self.bigBetState == 0:
            self.bal = self.bal - 100
            self.Bots = []
            self.Bots.append(Bot(200, self.cashOut, self.NumLives, self.Multiplier))
            self.bigBetState = 1
        elif self.Bots[-1].failed == 1 and self.bigBetState == 1:
            self.bal = 0
            self.failed = 1
            self.Bots = []
        else:
            if self.Bots[-1].hasDoubled == 1:
                self.bal = self.bal + self.Bots[-1].stableBal
                self.Bots = []
                self.bigBetState = 0
                self.Bots.append(Bot(100, self.cashOut, self.NumLives, self.Multiplier))
            
            if self.bal >= 600:
                #print("Big Bot doubled")
                self.hasDoubled = 1
        

            
   


        




class Bot():
    def __init__(self, Balance, CashOut, NumLives, Multiplier):
        self.bal = Balance
        self.cashOut = CashOut
        self.NumLives = NumLives
        self.Multiplier = Multiplier
        self.lossStreak = 0
        self.usingBal = self.bal
        self.flag = 0
        self.balMulti = 1
        self.stableBal = self.bal
        self.initialDivisor = self.genInitialDivisor(Multiplier)
        self.hasDoubled = 0
        self.numGames = 0
        self.failed = 0
    
    def runFinite(self, CrashValue):
        if self.bal >= 2*self.stableBal or self.hasDoubled == 1:
            self.hasDoubled = 1
            return
        elif self.failed == 1:
            return
        self.numGames+=1
        if float(CrashValue) < float(self.cashOut):
            self.lossStreak+=1
            if self.lossStreak >= self.NumLives:
                self.failed = 1
                return    
            self.bal = self.bal - self.genBetAmount(self.lossStreak-1)
        else:
            if self.bal < 0:
                return                
            self.bal = self.bal + self.genBetAmount(self.lossStreak)*(self.cashOut-1)   
            self.usingBal = self.bal
            self.lossStreak = 0
    
        
    def genMultiplier(self):
        var = self.cashOut - 1
        var = var * 2
        return ((var + 1)/(self.cashOut-1))

    def genInitialDivisor(self, Multiplier):
        BetAmounts = [None]*self.NumLives
        BetAmounts[0] = 1
        for counter in range(1,self.NumLives):
            BetAmounts[counter] = Multiplier * BetAmounts[counter-1]
        TotalBets = sum(BetAmounts)
        return BetAmounts[self.NumLives-1]/TotalBets


    def genBetAmount(self, LossStreak):
        initialDivisor = self.initialDivisor
        balance = self.usingBal* 0.99
        BetAmounts = [0.0] * self.NumLives
        BetAmounts[0] = balance * initialDivisor
        for counter in range(1,self.NumLives):
            BetAmounts[counter] = BetAmounts[counter-1]/self.Multiplier

        if (self.NumLives-1)-LossStreak >= 0:
            return round(BetAmounts[(self.NumLives-1)-LossStreak],4)
        else:
            return 0


    


class GameBot():
    def __init__(self):
        self.BotList = []
        self.History = []
    
    def addBot(self, Balance, cashOut, NumLives, Multiplier):
        newBot = Bot(Balance, cashOut, NumLives, Multiplier)
        self.BotList.append(newBot)
    
    def createHistory(self):
        self.History = open("stats3.txt").readlines()
        self.History = [word.strip() for word in self.History]
        self.History = [float(i) for i in self.History]


    def findStreak(self):
        biggestStreak = 0
        value = float(input("Enter limit value: "))
        currentStreak = 0
        inStreak = 0
        numberOfStreaks = 1
        for element in self.History:  
            if inStreak == 1:
                if element >= value:
                    inStreak = 0
                    currentStreak = 0
                else:
                    currentStreak+=1
            elif element < value:
                inStreak = 1
                currentStreak = 1
            if currentStreak > biggestStreak:
                biggestStreak = currentStreak
                numberOfStreaks = 1
            elif currentStreak == biggestStreak:
                numberOfStreaks+=1
                
        print(biggestStreak)
        print("The biggest Streak of values below " + str(value) + " was: " + str(biggestStreak))
        print("This streak happened " + str(numberOfStreaks) + "times")

    def runLimited(self, limitNumber):
        firstNum = random.randint(0,len(self.History) - limitNumber)
        tempHistory = []
        for counter in range(firstNum, firstNum + limitNumber):
            tempHistory.append(self.History[counter])
            
        for CrashScore in tempHistory:
            for Bot in self.BotList:
                Bot.runFinite(CrashScore)
               

    def runChanceOfDouble(self):
        testingcashout = [1.7,2,2.2,2.4]
        testingNumLives = [3,4,5,6,7,8,9,10,11,12,13,14]
        testingMultis = [2,3,4,5,6,7,8,9,10]
        total = 0.00
        numGames = 0
        for multi in testingMultis:
            for cashOut in testingcashout:
                for numLives in testingNumLives:
                    numGames = 0
                    currentHighest = 0
                    for counter in range(0,50):
                        self.BotList.append(DoubleBot(300,cashOut,numLives,multi))
                        self.runLimited(10000)
                        if self.BotList[-1].hasDoubled == 1:
                            total+=1
                            numGames+= self.BotList[-1].numGames
                            if currentHighest < self.BotList[-1].numGames:
                                currentHighest = self.BotList[-1].numGames
                        self.BotList = []
                    tempTotal = total
                    total = (total/50)*100
                    
                    if total >= 50.0:
                        print("Multi: " + str(multi) + " cashOut: " + str(cashOut) + " NumLives: " + str(numLives) + " AvgGame: " + str(round(numGames/tempTotal)) +  " " + bcolors.OKGREEN + str(total) + "%" + bcolors.ENDC)
                        print("\n")

                    elif total > 0:
                        print("Multi: " + str(multi) + " cashOut: " + str(cashOut) + " NumLives: " + str(numLives) + " AvgGameLength: " + str(round(numGames/tempTotal)) +  " " + bcolors.FAIL + str(total) + "%" + bcolors.ENDC)
                        print("\n")
                    total = 0.0
       
            
        
    
    

GameBot = GameBot()
GameBot.createHistory()
#GameBot.addBot(1000,1.5,10)
#GameBot.addBot(1000,1.7,10)
#GameBot.addBot(1000,10,50)
#GameBot.addBot(1000,3,40)
#GameBot.addBot(1000,2,10,4)
#GameBot.addBot(1000,2,11,2)
#GameBot.addBot(1000,2,10,3)
#GameBot.addBot(1000,2,12,2)
#GameBot.addBot(100,2,15,2)
#GameBot.addBot(1000,2,12,3)



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'