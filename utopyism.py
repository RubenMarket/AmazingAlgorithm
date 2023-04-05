from serverconfig import *

db = client.Utopyism
News = db.News
Voting = db.Voting

# Voting = db.Voting

# def initVoting():
#     return {
#             "_id" : "VoteCounts",
#             "LowVote" : 0,
#             "MidVote" : 0,
#             "HighVote" : 0
#         }
    
# initvote = initVoting()

# def initNews():
#     return {
#             "_id" : "AllNews",
#             "firstNews" : "Utopyism Under Development",
#             "secondNews" : ""
#         }
    
# initNews = initNews()

#####################################
TotalProfit = 0
# Total Profit this period(2 weeks)
GrossSales = 0
# Gross Sales this period(2 weeks)
PrevProfitCap = 0
# Prev Profit Cap
PrevBasicIncome = 0
# Previous Weeks Basic Income(before dispersed)
ProfitCap = 0
# Winning Profit Cap(12:00am)
BasicIncome = 0
# Lump sum of profit minus its cap(friday 12:00am)
######################################
# Databse Data
AccountHolders = 0
# Number of Accounts in Database
hasVotingEnded = False
# 12:00am Monday
votingInfo = Voting.find_one({"_id" : "VoteCounts"})
LowVotes = votingInfo['LowVote']
MidVotes = votingInfo['MidVote']
HighVotes = votingInfo['HighVote']
# Votes for each option
#######################################


def updateEarningsInfo(a, b, c, d):
    print("Company Profit After Expenses")
    print(a)
    print("Company Gross/Total Sales Before Expenses")
    print(b)
    print("Previous Weeks Profit Max/Cap")
    print(c)
    print("Amount Given to Basic Income last cycle")
    print(d)
    return


def calcvotingnumbers(a, b, c, d):
    votevalues = [a, b, c, d]
    votevalues.sort()
    # Sorting values from smallest to largest

    newvote1 = (votevalues[0] + votevalues[1]) / 2
    print("first/smallest voting option")
    print(newvote1)
    # smallest/first voting number
    newvote2 = (votevalues[1] + votevalues[2]) / 2
    print("second/middlest voting option")
    print(newvote2)
    # middle/second voting number
    newvote3 = (votevalues[2] + votevalues[3]) / 2
    print("third/largest voting option")
    print(newvote3)
    # largest/third voting number

    return


def emptyShopTrashCan():
    #set shop trash awecoin to 0
    return

def calcUBI(x, y, a, b):
    # x = number of accounts in database , y = personalawecoin
    # a = profit(total) , b = profit cap(voted)
    print("Personal AweCoin")
    print(y)
    if a >= b:
        UBI = a - b
        BI = UBI / x
        print("Basic Income Per Person")
        print(BI)
        MyNewAwecoin = y + BI
        print("New AweCoin Total")
        print(MyNewAwecoin)
        # Setting the New Awe Coin(database)
    else:
        print("Less Profit Than The Cap")
        MyNewAwecoin = y
        print("New AweCoin Total(same as prev)")
        print(MyNewAwecoin)
        # Setting the New Awe Coin(database)
    return


if hasVotingEnded is True:

    calcvotingnumbers(PrevProfitCap, GrossSales, TotalProfit, PrevBasicIncome)

    calcUBI(AccountHolders, MyAwecoin, TotalProfit, ProfitCap)

# Information PAGE
updateEarningsInfo(TotalProfit, GrossSales, PrevProfitCap, PrevBasicIncome)

showlivecount(votesfor1, votesfor2, votesfor3)
