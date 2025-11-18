import math

def change(amount, coins):
    """Return a non-negative integer indicating the minimum number of coins required to make up the given amount. 

    Parameters:
        amount: int
            a non-negative integer indicating the amount of change to be made
        coins: list
            a list of coin values
            
    Returns:
        int:
            a non-negative integer indicating the minimum number of coins required to make up the given amount.
    
    Examples:
        >>> change(48, [1, 5, 10, 25, 50])
        6
        >>> change(48, [1, 7, 24, 42])
        2
        >>> change(35, [1, 3, 16, 30, 50])
        3
        >>> change(6, [4, 5, 9])
        math.inf
    """
    if amount == 0:
        return 0
    if amount < 0 or not coins:
        return math.inf
    
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for x in range(1, amount+1):
        for coin in coins:
            if x-coin >= 0:
                dp[x] = min(dp[x], dp[x-coin] + 1)
    
    return dp[amount]


def giveChange(amount, coins):
    """Return a list with the minimum number of coins(int) and  a list of the coins in the optimal solution.

    Parameters:
        amount: int
            a non-negative integer indicating the amount of change to be made
        coins: list
            a list of coin values
        
    Returns:
        list:
            a list whose first member is the minimum number of coins(int) and whose second member is a list of the coins in the optimal solution.
    
    Examples:
        >>> giveChange(48, [1, 5, 10, 25, 50])
        [6, [25, 10, 10, 1, 1, 1]]
        >>> giveChange(48, [1, 7, 24, 42])
        [2, [24, 24]]
        >>> giveChange(35, [1, 3, 16, 30, 50])
        [3, [16, 16, 3]]
        >>> giveChange(6, [4, 5, 9])
        [math.inf, []]
    """
    if amount == 0:
        return [0, []]
    if amount < 0 or not coins:
        return [math.inf, []]
    
    dp = [float("inf")] * (amount+1)
    usedCoin = [float("inf")] * (amount+1)
    
    dp[0] = 0
    
    for x in range(1, amount+1):
        for coin in coins:
            if x-coin >= 0:
                if dp[x] > dp[x-coin] + 1:
                    dp[x] = dp[x-coin] + 1
                    usedCoin[x] = coin
    
    if dp[amount] == float("inf"):
        return [math.inf, []]
    
    usedCoins = []
    i = amount
    while i > 0:
        usedCoins.append(usedCoin[i])
        i -= usedCoin[i]
    
    usedCoins.reverse()
    
    return [dp[amount], usedCoins]
    
