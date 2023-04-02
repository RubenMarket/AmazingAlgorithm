Utopyism Algorithm

A Profit Maximum Company

Biweekly/weekly/quarterly profit max/cap vote

even distribution of cryptocurrency to all participants of company holding an account with them

repeat


How are the voting numbers calculated?
there are always 3 voting options

take 4 variables(total/gross sales,Profit/Income,previous amount distributed to particpants,previous winning voting number)

order them from least to greatest in number

   |------|------|------|

least                 greatest


the median between each number are the options( 3 total )


to begin, previous amount distributed to particpants and previous winning votng number equals 0



Money earned over voted profit max gets directly injected into products
 or services that participants can buy with their cryptocurrency















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
votesfor1 = 0
votesfor2 = 0
votesfor3 = 0
# Votes for each option
#######################################
# User Specific Information
MyAwecoin = 0
isAweMember = True
hasVoted = False
personalidentifier = 0


def showlivecount(x, y, z):
    # showing count on info page
    votesfor1label = x
    print(votesfor1label)
    votesfor2label = y
    print(votesfor2label)
    votesfor3label = z
    print(votesfor3label)
    # update labels on count
    return


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
