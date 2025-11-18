# you may use pandas only for IO reason
# Using it to do sort will impact your grade
# import pandas as pd
import random
import timeit
import csv


def timeFunc(method):
    """
    Define the main body of the decorator that decorates a method.
        
    Returns
    -------
    Callable
        A wrapper that defines the behavior of the decorated method
    """
    def wrapper(*args, **kwargs):
        """
        Define the behavior of the decorated method
        Parameters:
            Same as the parameters used in the methods to be decorated
            
        Returns:
            Same as the objects returned by the methods to be decorated
        """
        start = timeit.default_timer()
        result = method(*args, **kwargs)  
        # record the time consumption of executing the method
        time = timeit.default_timer() - start
        
        # send metadata to standard output
        print(f"Method: {method.__name__}")
        print(f"Result: {result}")
        print(f"Elapsed time of 10000 times: {time*10000} seconds")
        return result
    return wrapper


class MusicLibrary:
    def __init__(self):
        """
        Initialize the MusicLibrary object with default values.
        self.data the collect of music library
        self.rows: the row number 
        self.cols: the col number 
        self.nameIndex: the number represent the index of name in each element of self.data
        self.albumIndex: the number represent the index of album in each element of self.data
        self.trackIndex: the number represent the index of track in each element of self.data
        """
        self.data = []
        self.rows = 0
        self.cols = 0
        self.nameIndex = 0
        self.albumIndex = 1
        self.trackIndex = 1

    def readFile(self, fileName):
        """
        Read music data from a CSV file and store it in the self.data attribute.
        The self.rows and self.cols should be updated accordingly. 
        The self.data should be [[name, albums count, tract count],...]
        You could assume the file is in the same directory with your code.
        Please research about the correct encoding for the given data set, 
        as it is not UTF-8.
        You are allowed to use pandas or csv reader, 
        but self.data should be in the described form above.

        Parameters
        ----------
        fileName : str
            The file name of the CSV file to be read.
        """
        f = open(fileName, mode = "r", encoding="ISO-8859-1")
        reader = csv.reader(f)
        for row in reader:
            name = row[0].strip()
            albums = int(row[1].strip())
            tracks = int(row[2].strip())
            self.data.append([name, albums, tracks])
        
        self.rows = len(self.data)
        self.cols = 3        
        
        f.close()

    def printData(self):
        """
        Print the data attribute stored in the library instance in a formatted manner.
        """
        for row in self.data:
            print(row)

    def shuffleData(self):
        """
        Shuffle the data stored in the library.
        refer to the random package
        """
        random.shuffle(self.data)
    
    def _binarySearchHelper(self,key, keyIndex, left, right):
        """
        Perform binary search recursively. 
        
        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.
        left: int
            The left boundary. 
        right: int
            The right boundary.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        # If not found, return -1. 
        if left > right:
            return -1
        
        mid = (left + right) // 2
        
        if key == self.data[mid][keyIndex]:
            return mid
        elif key < self.data[mid][keyIndex]: # In the left part. 
            return self._binarySearchHelper(key, keyIndex, left, mid-1)
        else: # In the right part. 
            return self._binarySearchHelper(key, keyIndex, mid+1, right)

    @timeFunc
    def binarySearch(self, key, keyIndex):
        """
        Perform a binary search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        return self._binarySearchHelper(key, keyIndex, 0, len(self.data)-1)

    @timeFunc
    def seqSearch(self, key, keyIndex):
        """
        Perform a sequential search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        for i in range(self.rows):
            if self.data[i][keyIndex] == key:
                return i
        
        return -1

    @timeFunc
    def bubbleSort(self, keyIndex):
        """
        Sort the data using the bubble sort algorithm based on a specific column index.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        for i in range(self.rows):
            swapped = False
            for j in range(self.rows-1-i):
                if self.data[j][keyIndex] > self.data[j+1][keyIndex]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
                    swapped = True
            if not swapped:
                break

    def merge(self, L, R, keyIndex):
        """
        Merge two sorted sublists into a single sorted list.
        This is the helper function for merge sort.
        You may change the name of this function or even not have it.
        

        Parameters
        ----------
        L, R : list
            The left and right sublists to merge.
        keyIndex : int
            The column index to sort by.

        Returns
        -------
        list
            The merged and sorted list.
        """
        # Implementation details...
        merged = []
        len1 = len(L)
        len2 = len(R)
        i = 0
        j = 0
        
        while i < len1 and j < len2:
            if L[i][keyIndex] < R[j][keyIndex]:
                merged.append(L[i])
                i += 1
            else:
                merged.append(R[j])
                j += 1
        
        while i < len1:
            merged.append(L[i])
            i += 1
        while j < len2:
            merged.append(R[j])
            j += 1
        
        return merged
        

    @timeFunc
    def mergeSort(self, keyIndex):
        """
        Sort the data using the merge sort algorithm.
        This is the main mergeSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        self.data = self._mergeSort(self.data, keyIndex)

    def _mergeSort(self, arr, keyIndex):

        # This is the helper function for merge sort.
        # You may change the name of this function or even not have it.
        # This is a helper method for mergeSort
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        L = self._mergeSort(arr[:mid], keyIndex)
        R = self._mergeSort(arr[mid:], keyIndex)
        
        return self.merge(L, R, keyIndex)

    @timeFunc
    def quickSort(self, keyIndex):
        """
        Sort the data using the quick sort algorithm.
        This is the main quickSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        # Implementation details...
        return self._quickSort(self.data, 0, self.rows-1, keyIndex)

    def _partition(self, arr, low, high, keyIndex):
        pivot = arr[high][keyIndex]
        leftWall = low
        
        for i in range(low, high):
            if arr[i][keyIndex] <= pivot:
                arr[i], arr[leftWall] = arr[leftWall], arr[i]
                leftWall += 1
        
        arr[leftWall], arr[high] = arr[high], arr[leftWall]
        return leftWall

    def _quickSort(self, arr, low, high, keyIndex):
        # This is a helper method for quickSort
        # ...
        if low < high:
            pi = self._partition(arr, low, high, keyIndex)
            if pi > 0:
                self._quickSort(arr, low, pi-1, keyIndex)
            self._quickSort(arr, pi+1, high, keyIndex)

    def comment(self):
        '''
        Based on the result you find about the run time of calling different function,
        Write a small paragraph (more than 50 words) about time complexity, and print it. 
        '''
        # print(you comment)
        print("Based on this assignment, we know that sequence search needs O(n) time while "
                "binary search runs in O(log n) time after sorting. For different sorting methods, "
                "we can find that bubble sort is obviously slower (O(n^2)) than other methods, while "
                "merge sort and quick sort are much faster, both average time consumption is "
                "O(n log n). However, quick sort's worst case time is O(n^2). Therefore, we cannot "
                "determine exactly which sort is the most efficient, and it really depends.")



# create instance and call the following instance method
# using decroator to decroate each instance method
def main():
    random.seed(42)
    myLibrary = MusicLibrary()
    filePath = 'music.csv'
    myLibrary.readFile(filePath)

    idx = 0
    myLibrary.data.sort(key = lambda data: data[idx])
    myLibrary.seqSearch(key="30 Seconds To Mars", keyIndex=idx)
    myLibrary.binarySearch(key="30 Seconds To Mars", keyIndex=idx)

    idx = 2
    myLibrary.shuffleData()
    myLibrary.bubbleSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.quickSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.mergeSort(keyIndex=idx)
    myLibrary.printData()

if __name__ == "__main__":
    main()

