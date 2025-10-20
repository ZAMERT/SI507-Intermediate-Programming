from enum import Enum

'''
This is the start of the HW.
If there is any conflict between the doc string and the HW document,
please follow the instruction in the HW document.
Good Luck and have fun !
'''

class Notation(Enum):
    """Enumeration for representing different types of notations in the game.

    Attributes:
        EMPTY (int): Represents an empty cell on the board.
        PLAYER1 (int): Represents a cell occupied by Player 1.
        PLAYER2 (int): Represents a cell occupied by Player 2.
    """
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2
    

class Player:
    """Represents a player in the game.

    Attributes:
        __playerName (str): The name of the player.
        __playerNotation (Notation): The notation (symbol) used by the player on the board.
        __curScore (int): The current score of the player.

    Args:
        playerName (str): The name of the player.
        playerNotation (Notation): The notation (symbol) used by the player.
        curScore (int): The initial score of the player.
    """

    def __init__(self, playerName, playerNotation, curScore) -> None:
        self.__playerName = playerName
        self.__playerNotation = playerNotation
        self.__curScore = curScore

    def display(self) -> str:
        """Displays the player's details including name, notation, and current score."""
        details = f"Player Name: {self.__playerName}, Current Score: {self.__curScore}, Player Notation: {self.__playerNotation.name}"
        print(details)
        return details

    def addScoreByOne(self) -> None:
        """Increments the player's score by one."""
        self.__curScore += 1

    def getScore(self) -> int:
        """Returns the current score of the player."""
        return self.__curScore

    def getName(self) -> str:
        """Returns the name of the player."""
        return self.__playerName

    def getNotation(self) -> Notation:
        """Returns the notation used by the player."""
        return self.__playerNotation

class Board:
    """Represents the game board.

    Attributes:
        __rowNum (int): Number of rows in the board.
        __colNum (int): Number of columns in the board.
        __grid (list): 2D list representing the game board.

    Args:
        rowNum (int): Number of rows in the board.
        colNum (int): Number of columns in the board.
    """

    def __init__(self, rowNum, colNum) -> None:
        self.__rowNum = rowNum
        self.__colNum = colNum
        self.__grid = []
        self.initGrid()

    def initGrid(self) -> None:
        """Initializes the game board with empty cells."""
        self.__grid = [[Notation.EMPTY for _ in range(self.__colNum)] for _ in range(self.__rowNum)]

    def getColNum(self) -> int:
        """Returns the number of columns in the board."""
        return self.__colNum

    def placeMark(self, colNum, mark) -> bool:
        """Attempts to place a mark on the board at the specified column.

        Args:
            colNum (int): The column number where the mark is to be placed.
            mark (Notation): The mark to be placed on the board.

        Returns:
            bool: True if the mark was successfully placed, False otherwise.
        """
        if self.getColNum() <= colNum or colNum < 0: # Check if the provided colNum is valid. 
            print(f"Column number {colNum} is out of range.")
            return False
        if self.__grid[0][colNum] != Notation.EMPTY: # Check if the top cell of the specified column is already filled.
            print("column is full")
            return False
        if mark == Notation.EMPTY: # Check if the provided mark is valid.
            print("invalid marker")
            return False
        for row in range(self.__rowNum-1, -1, -1): # Iterate through the cells of the specified column from bottom to top. 
            if self.__grid[row][colNum] == Notation.EMPTY:
                self.__grid[row][colNum] = mark # Place the mark in the first empty cell found. 
                return True
        return False
        

    def checkFull(self) -> bool:
        """Checks if the board is completely filled.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        for col in range(self.__colNum):
            if self.__grid[0][col] == Notation.EMPTY:
                return False
        return True

    def display(self) -> None:
        """Displays the current state of the board."""
        boardStr = ""
        for row in range(self.__rowNum):
            for col in range(self.__colNum):
                if self.__grid[row][col] == Notation.EMPTY:
                    boardStr += "O"
                elif self.__grid[row][col] == Notation.PLAYER1:
                    boardStr += "R"
                elif self.__grid[row][col] == Notation.PLAYER2:
                    boardStr += "Y"
            boardStr += "\n"
        print("Current Board is: \n" + boardStr)

    # Private methods for internal use
    def __checkWinHorizontal(self, target) -> Notation | None:
        for row in range(self.__rowNum):
            for col in range(self.__colNum - target + 1):
                first_cell = self.__grid[row][col]
                if first_cell == Notation.EMPTY:
                    continue
                win = True
                for test in range(1, target):
                    if self.__grid[row][col+test] != first_cell:
                        win = False
                        break
                if win:
                    return first_cell
        return None

    def __checkWinVertical(self, target) -> Notation | None:
        for col in range(self.__colNum):
            for row in range(self.__rowNum - target + 1):
                first_cell = self.__grid[row][col]
                if first_cell == Notation.EMPTY:
                    continue
                win = True
                for test in range(1, target):
                    if self.__grid[row + test][col] != first_cell:
                        win = False
                        break
                if win:
                    return first_cell
        return None

    def __checkWinOneDiag(self, target, rowNum, colNum) -> Notation | None:
        if rowNum + target > self.__rowNum or colNum + target > self.__colNum:
            return None
        first_cell = self.__grid[rowNum][colNum]
        if first_cell == Notation.EMPTY:
            return None
        for test in range(1, target):
            if self.__grid[rowNum + test][colNum + test] != first_cell:
                return None
        return first_cell

    def __checkWinAntiOneDiag(self, target, rowNum, colNum) -> Notation | None:
        if rowNum + target > self.__rowNum or colNum - (target - 1) < 0:
            return None
        first_cell = self.__grid[rowNum][colNum]
        if first_cell == Notation.EMPTY:
            return None
        for test in range(1, target):
            if self.__grid[rowNum + test][colNum - test] != first_cell:
                return None
        return first_cell

    def __checkWinDiagonal(self, target) -> Notation | None:
        for row in range(self.__rowNum):
            for col in range(self.__colNum):
                test = self.__checkWinOneDiag(target, row, col)
                if test:
                    return test
                test2 = self.__checkWinAntiOneDiag(target, row, col)
                if test2:
                    return test2
        return None

    def checkWin(self, target) -> Notation | None:
        """Checks if there is a winning condition on the board.

        Args:
            target (int): The number of consecutive marks needed for a win.

        Returns:
            Notation or None: The notation of the winning player, or None if there is no winner.
        """
        return (self.__checkWinHorizontal(target) or self.__checkWinVertical(target) or self.__checkWinDiagonal(target))

class Game:
    """Represents the game logic and flow.

    Args:
        rowNum (int): Number of rows in the game board.
        colNum (int): Number of columns in the game board.
        connectN (int): Number of consecutive marks needed for a win.
        targetScore (int): The score a player needs to reach to win the game.
        playerName1 (str): Name of the first player.
        playerName2 (str): Name of the second player.
    """

    def __init__(self, rowNum, colNum, connectN, targetScore, playerName1, playerName2) -> None:
        self.__board = Board(rowNum, colNum)
        self.__connectN = connectN
        self.__targetScore = targetScore
        self.__playerList = [Player(playerName1, Notation.PLAYER1, 0), Player(playerName2, Notation.PLAYER2, 0)]
        self.__curPlayer = self.__playerList[0]

    def __playBoard(self, curPlayer) -> None:
        """Handles the process of a player making a move on the board.

        Args:
            curPlayer (Player): The current player who is making the move.
        """
        isPlaced = False
        while not isPlaced:
            try:
                col_Num = input(f"{curPlayer.getName()}, please input a column number between 0 and {self.__board.getColNum() - 1}: ")
                if not col_Num.isdigit():
                    print("Invalid. Please enter a valid integer.")
                    continue
                if len(col_Num) > 1 and col_Num[0] == '0':
                    print("Invalid. Please enter a valid integer.")
                    continue
                col_Num = int(col_Num)
                isPlaced = self.__board.placeMark(col_Num, curPlayer.getNotation())
            except ValueError:
                print("Invalid. Please enter a valid integer.")
                continue

    def __changeTurn(self) -> None:
        """Switches the turn to the other player."""
        if self.__curPlayer == self.__playerList[0]:
            self.__curPlayer = self.__playerList[1]
        else:
            self.__curPlayer = self.__playerList[0]

    def playRound(self) -> None:
        """Plays a single round of the game."""
        curWinnerNotation = None
        self.__board.initGrid()
        self.__curPlayer = self.__playerList[0]
        print("Starting a new round")
        while not curWinnerNotation:
            self.__curPlayer.display()
            self.__board.display()
            self.__playBoard(self.__curPlayer)
            curWinnerNotation = self.__board.checkWin(self.__connectN)
            if curWinnerNotation:
                print(f"{self.__curPlayer.getName()} wins this round!")
                self.__board.display()
                self.__curPlayer.addScoreByOne()
                break
            if self.__board.checkFull():
                print("The board is full. No winner for this round.")
                break
            self.__changeTurn()

    def play(self) -> None:
        """Starts and manages the game play until a player wins."""
        reachTarget = False
        while not reachTarget:
            self.playRound()
            for player in self.__playerList:
                if player.getScore() >= self.__targetScore:
                    reachTarget = True
                    break
        print("Game Over")
        for player in self.__playerList:
            player.display()
"""
############################## Homework ConnectN ##############################

% Student Name: Yuchen Liu

% Student Unique Name: ylyuchen

% Lab Section 00X: 

% I worked with the following classmates: 

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

def main():
    """Main function to start the game."""
    game = Game(4, 4, 3, 2, 'P1', 'P2')
    game.play()

if __name__ == "__main__":
    main()
