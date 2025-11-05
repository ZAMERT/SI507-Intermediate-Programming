class TwentyQuestions:
    def __init__(self):
        """
        Initialize the TwentyQuestions class with predefined small and medium trees.
        Sets the current tree to the small tree by default.
        """
        self.smallTree = (
            "Is it bigger than a breadbox?",
            ("an elephant", None, None),
            ("a mouse", None, None),
        )
        self.mediumTree = (
            "Is it bigger than a breadbox?",
            ("Is it gray?", ("an elephant", None, None), ("a tiger", None, None)),
            ("a mouse", None, None),
        )
        self.currentTree = self.smallTree  # Default tree

    def inputChecker(self, userIn: str) -> bool:
        """
        aka(yes(userIn))
        Check if the user's input is an affirmative response.

        Parameters
        ----------
        userIn : str
            The input string from the user.

        Returns
        -------
        bool
            True if the input is an affirmative response ('y', 'yes', 'yup', 'sure'), else False.
        """
        affirmativeResponse = ['y', 'yes', 'yup', 'sure']
        return userIn.strip().lower() in affirmativeResponse

    def checkIfLeaf(self, curNode) -> bool:
        """
        Determine if the given node is a leaf node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the node is a leaf (both children are None), else False.
        """
        if curNode is None:
            return False
        _, left, right = curNode
        return left is None and right is None

    def simplePlay(self, curNode) -> bool:
        """
        Conduct a simple play-through of the game using the current node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the player successfully guesses the item, else False.
        """
        tree, left, right = curNode
        
        # Check if the tree is a leaf.
        if self.checkIfLeaf(curNode): # Is leaf. 
            answer = input(f"Is it {tree}? ")
            return self.inputChecker(answer)
        
        else: # Not leaf. 
            # Ask the question in the tree. 
            answer = input(f"{tree} ")
            
            if self.inputChecker(answer): # If the user answers "yes".
                return self.simplePlay(left)
            else: # If the user answers "no". 
                return self.simplePlay(right)

    def createNode(self, userQuestion: str, userAnswer: str, isCorrectForQues: bool, curNode: tuple) -> tuple:
        """
        Create a new node in the decision tree.

        Parameters
        ----------
        userQuestion : str
            The question to differentiate the new answer from the current node.
        userAnswer : str
            The answer provided by the user.
        isCorrectForQues : bool
            True if the userAnswer is the correct response to the userQuestion.
        curNode : tuple
            The current node in the decision tree at which the game has arrived. 
            This node typically represents the point in the game 
            where the player's guess was incorrect, 
            and a new question-answer pair needs to be 
            added to refine the tree. 


        Returns
        -------
        tuple
            The new node created with the user's question and answer 
            and curNode
        """
        if isCorrectForQues:
            return (userQuestion, (userAnswer, None, None), curNode)
        else:
            return (userQuestion, curNode, (userAnswer, None, None))

    def playLeaf(self, curNode) -> tuple:
        """
        Handle gameplay when a leaf node is reached in the decision tree. This method is called when 
        the game's traversal reaches a leaf node, indicating a guess at the player's thought. 
        If the guess is incorrect, the method will
        1. prompts the player for the correct answer 
        2. prompts the player for a distinguishing question
        3. ask user what is the answer for the new input item to this distinguishing question(refer the io result of play in the homework doc)
            notice the node should follow (tree question, (node for answer yes), (node for answer no))
        4. creating a new node in the tree for future gameplay. It should call self.createNode(...)

        Parameters
        ----------
        curNode : tuple
            The current leaf node in the decision tree. A leaf node is represented as a tuple with the guessed 
            object as the first element and two `None` elements, signifying that it has no further branches.

        Returns
        -------
        tuple
            The updated node based on user input. If the player's response indicates that the initial guess was 
            incorrect, this method returns a new node that includes the correct answer and a new question 
            differentiating it from the guessed object. If the guess was correct, it simply returns the unchanged 
            `curNode`.
        
        Notes
        -----
        The method interacts with the player to refine the decision tree. It's a crucial part of the learning 
        aspect of the game, enabling the tree to expand with more nuanced questions and answers based on 
        player feedback.
        """
        guess, _, _ = curNode
        ans = input(f"Is it {guess}? ")
        # If the guess is correct. 
        if self.inputChecker(ans): 
            print("I got it!")
            return curNode
        else:
            correctAns = input("Drats! What was it? ")
            question = input(f"What's a question that distinguishes between {correctAns} and {guess}? ")
            newAns = input(f"And what's the answer for {correctAns}? ")
            newNode = self.createNode(question, correctAns, self.inputChecker(newAns), curNode)
            return newNode
        


    def play(self, curNode) -> tuple:
        """
        Conduct gameplay starting from the given node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        tuple
            The updated tree after playing from the given node.
        """
        tree, left, right = curNode
        # Check if the node is leaf.
        if self.checkIfLeaf(curNode):
            return self.playLeaf(curNode)
        else: 
            ans = input(f"{tree}")
            if self.inputChecker(ans):
                newLeft = self.play(left)
                return (tree, newLeft, right)
            else:
                newRight = self.play(right)
                return (tree, left, newRight)

    def playRound(self) -> None:
        """
        Execute a single round of the game, starting from the current state of the currentTree attribute. This method 
        calls the 'play' method to navigate through the tree. It then updates the 'currentTree' 
        attribute with the potentially modified tree resulting from this round of gameplay.


        Returns
        -----
        None
        """
        self.currentTree = self.play(self.currentTree)


    def saveTree(self, node, treeFile) -> None:
        """
        Recursively save the decision tree to a file.

        Parameters
        ----------
        node : tuple
            The current node in the decision tree.
        treeFile : _io.TextIOWrapper
            The file object where the tree is to be saved.
        """
        if node is None:
            return
        tree, left, right = node
        # If the current node is leaf.
        if self.checkIfLeaf(node):
            treeFile.write(f"Leaf\n{tree}\n")
        else:
            treeFile.write(f"Internal node\n{tree}\n")
            self.saveTree(left, treeFile)
            self.saveTree(right, treeFile)

    def saveGame(self, treeFileName) -> None:
        """
        Save the current state of the game's decision tree to a specified file. This method opens the file 
        with the given filename and writes the structure of the current decision tree to it. The tree is saved 
        in a txt format.

        The method uses the 'saveTree' function to perform the recursive traversal and writing of the tree 
        structure. Each node of the tree is written to the file with its type ('Leaf' or 'Internal node') 
        followed by its content (question or object name). 

        Important: the format of the txt file should be exactly the same as the ones in our doc to pass the autograder. 
        
        Parameters
        ----------
        treeFileName : str
            The name of the file where the current state of the decision tree will be saved. The file will be 
            created or overwritten if it already exists.

        """
        f = open(treeFileName, mode = "w")
        self.saveTree(self.currentTree, f)
        f.close()


    def loadTree(self, treeFile) -> tuple:
        """
        Recursively read a binary decision tree from a file and reconstruct it.

        Parameters
        ----------
        treeFile : _io.TextIOWrapper
            An open file object to read the tree from.

        Returns
        -------
        tuple
            The reconstructed binary tree.
        """
        line = treeFile.readline().strip()
        if not line:
            return
        tree = treeFile.readline().strip()
        if line == "Leaf":
            return (tree, None, None)
        else:
            left = self.loadTree(treeFile)
            right = self.loadTree(treeFile)
            return (tree, left, right)

    def loadGame(self, treeFileName) -> None:
        """
        Load the game state from a specified file and update the current decision tree. This method opens the 
        file with the given filename and reconstructs the decision tree based on its contents. 

        The method employs the 'loadTree' function to perform recursive reading of the tree structure from the 
        file. Each node's type ('Leaf' or 'Internal node') and content (question or object name) are read and 
        used to reconstruct the tree in memory. This restored tree becomes the new 'self.currentTree' of the game.

        Parameters
        ----------
        treeFileName : str
            The name of the file from which the game state will be loaded. The file should exist and contain a 
            previously saved decision tree.

        """
        treeFile = open(treeFileName, mode = "r")
        self.currentTree = self.loadTree(treeFile)
        treeFile.close()


    def printTree(self):
        self._printTree(tree = self.currentTree)

    def _printTree(self, tree, prefix = '', bend = '', answer = ''):
        """Recursively print a 20 Questions tree in a human-friendly form.
        TREE is the tree (or subtree) to be printed.
        PREFIX holds characters to be prepended to each printed line.
        BEND is a character string used to print the "corner" of a tree branch.
        ANSWER is a string giving "Yes" or "No" for the current branch."""
        text, left, right = tree
        if left is None  and  right is None:
            print(f'{prefix}{bend}{answer}It is {text}')
        else:
            print(f'{prefix}{bend}{answer}{text}')
            if bend == '+-':
                prefix = prefix + '| '
            elif bend == '`-':
                prefix = prefix + '  '
            self._printTree(left, prefix, '+-', "Yes: ")
            self._printTree(right, prefix, '`-', "No:  ")
"""
############################## Homework 20questions ##############################

% Student Name: Yuchen Liu

% Student Unique Name: ylyuchen

% Lab Section 00X: 1

% I worked with the following classmates: Nobody

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

def main():
    """
    Main function for the 20 questions game.
    """
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.
    
    game = TwentyQuestions()
    print("Welcome to 20 Questions!")
    
    isload = input("Would you like to load a tree from a file? ").strip().lower()
    if game.inputChecker(isload):
        fileName = input("What's the name of the file? ").strip()
        game.loadGame(fileName)
    else:
        print("Starting with the small default tree. ")
    
    while True:
        game.playRound()
        ifAgain = input("Would you like to play again? ")
        if not game.inputChecker(ifAgain):
            break
    
    ifSave = input("Would you like to save this tree for later? ")
    if game.inputChecker(ifSave):
        fileSave = input("Please enter a file name: ").strip()
        game.saveGame(fileSave)
        print("Thank you! The file has been saved. ")
    
    print("Bye!")

if __name__ == '__main__':
    main()
