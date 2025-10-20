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
    
    use_it = 1 + change(amount-coins[-1], coins)
    lose_it = change(amount, coins[:-1])
    
    return min(use_it, lose_it)

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
    
    use_it = giveChange(amount-coins[-1], coins)
    lose_it = giveChange(amount, coins[:-1])
    
    use_count = 1 + use_it[0]
    lose_count = lose_it[0]
    
    return [use_count, use_it[1] + [coins[-1]]] if use_count < lose_count else [lose_count, lose_it[1]]
