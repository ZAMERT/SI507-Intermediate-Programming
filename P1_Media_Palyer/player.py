from media import Media, Track, Movie
from linked_list import LinkedList
import json
class Player:
    """
    A media player class that manages a playlist of media.

    This class utilizes a doubly linked list (LinkedList) to store and manage media in a playlist.
    It provides methods for adding, removing, playing, and navigating through media.

    Attributes
    ----------
    playlist : LinkedList
        A doubly linked list that stores the media in the playlist.
    currentMediaNode : Node or None
        The current media being played, represented as a node in the linked list.
    """

    def __init__(self) -> None:
        """
        Initializes the Player with an empty playlist and None as currentMediaNode.
        """
        self.playlist = LinkedList()
        self.currentMediaNode = None
        

    def addMedia(self, media) -> None:
        """
        Adds a media to the end of the playlist.
        Set the currentMediaNode to the first node in the playlist, 
        if currentMediaNode is None. 

        Parameters
        ----------
        media : Media | Track | Movie 
            The media to add to the playlist.
        """
        self.playlist.append(media)
        if self.currentMediaNode is None:
            self.currentMediaNode = self.playlist.dummyHead.next
        

    def removeMedia(self, index) -> bool:
        """
        Removes a media from the playlist based on its index.
        You can assume the only invalid input is invalid index.
        Set the currentMediaNode to its next, if currentMediaNode is removed,
        and remember using _isNodeUnbound(self.currentMediaNode) to check if a link is broken.

        Parameters
        ----------
        index : int
            The index of the media to remove.

        Returns
        -------
        bool
            True if the media was successfully removed, False otherwise.
        """
        targetNode = self.playlist._getNode(index) # None if index is out of range. 
        # Since the only invalid input is invalid index, return False directly. 
        if targetNode is None:
            return False
        
        is_current = (targetNode == self.currentMediaNode)
        removed = self.playlist.deleteAtIndex(index)
        
        if is_current:
            self.currentMediaNode = targetNode.next
            if self.currentMediaNode == self.playlist.dummyTail:
                self.currentMediaNode = self.playlist.dummyHead.next
            if self.playlist.getSize() == 0:
                self.currentMediaNode = None
            if self.currentMediaNode and self.playlist._isNodeUnbound(self.currentMediaNode):
                return False
        
        return removed
        

    def next(self) -> bool:
        """
        Moves currentMediaNode to the next media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the next media, False otherwise.
        """
        if not self.currentMediaNode or self.currentMediaNode.next == self.playlist.dummyTail:
            return False
        
        self.currentMediaNode = self.currentMediaNode.next
        return True
        

    def prev(self) -> bool:
        """
        Moves currentMediaNode to the previous media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the previous media, False otherwise.
        """
        if not self.currentMediaNode or self.currentMediaNode.prev == self.playlist.dummyHead:
            return False
        
        self.currentMediaNode = self.currentMediaNode.prev
        return True
        

    def resetCurrentMediaNode(self) -> bool:
        """
        Resets the current media to the first media in the playlist,
        if the playlist contains at least one media. 

        Returns
        -------
        bool
            True if the current media was successfully reset, False otherwise.
        """
        if self.playlist.getSize() == 0:
            return False
        self.currentMediaNode = self.playlist.dummyHead.next
        return True
        

    def play(self) -> None:
        """
        Plays the current media in the playlist. 
        Call the play method of the media instance.
        Remember currentMediaNode is a node not a media, but its data is the actual
        media. If the currentMediaNode is None or its data is None, 
        print "The current media is empty.". 
        """
        if not self.currentMediaNode or not self.currentMediaNode.data:
            print("The current media is empty.")
            return
        self.currentMediaNode.data.play()
        
        

    def playForward(self) -> None:
        """
        Plays all the media in the playlist from front to the end,
        by iterating the linked list.  
        Remember each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print "Playlist is empty.". 
        """
        if self.playlist.getSize() == 0:
            print("Playlist is empty.")
            return 
        currMedia = self.playlist.dummyHead.next
        while currMedia != self.playlist.dummyTail:
            currMedia.data.play()
            currMedia = currMedia.next
        

    def playBackward(self) -> None:
        """
        Plays all the media in the playlist from the back to front,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print this string "Playlist is empty.". 
        """
        if self.playlist.getSize() == 0:
            print("Playlist is empty.")
            return 
        currMedia = self.playlist.dummyTail.prev
        while currMedia != self.playlist.dummyHead:
            currMedia.data.play()
            currMedia = currMedia.prev
        

    def loadFromJson(self, fileName) -> None:
        """
        Loads media from a JSON file and adds them to the playlist.
        The order should be the same as the provided json file. 
        You could assume the filename is always valid
        Notice, for each given json object, 
        you should create instance of the correct instance type, (movie,track,media).
        You need to observe the provided json and figure how to do it.
        You could assume if a json object is not track or movie,
        it has to be a media.
        Pay attention the name of the key in each json object. 
        Set the currentMediaNode to the first media in the playlist, 
        if there is at least one media in the playlist.
        Remeber to use the dictionary get method. 

        Parameters
        ----------
        filename : str
            The name of the JSON file to load media from.
        """
        with open(fileName, "r") as f:
            data = json.load(f)
            
        for item in data:
            kind = item.get("kind")
            itemTitle = item.get("trackName", "No Title")
            itemArtist = item.get("artistName", "No Artist")
            itemReleaseDate = item.get("releaseDate", "No Release Date")
            itemUrl = item.get("trackViewUrl", "No URL")
            itemLength = item.get("trackTimeMillis", 0)
            
            if kind == "feature-movie":
                newMedia = Movie(
                    title = itemTitle, 
                    artist = itemArtist, 
                    releaseDate = itemReleaseDate, 
                    url = itemUrl, 
                    rating = item.get("contentAdvisoryRating", "No Rating"), 
                    # movieLength = round(item.get("trackTimeMillis", 0) / 60000)
                    movieLength = itemLength
                )
            elif kind == "song":
                newMedia = Track(
                    title = itemTitle, 
                    artist = itemArtist, 
                    releaseDate = itemReleaseDate, 
                    url = itemUrl, 
                    album = item.get("collectionName", "No Album"), 
                    genre = item.get("primaryGenreName", "No Genre"), 
                    # duration = round(item.get("trackTimeMillis", 0) / 1000)
                    duration = itemLength
                )
            else:
                newMedia = Media(
                    title = item.get("collectionCensoredName", "No Title"), 
                    artist = itemArtist, 
                    releaseDate = itemReleaseDate, 
                    url = item.get("collectionViewUrl", "No URL")
                )
            
            self.playlist.append(newMedia)
        
        if self.playlist.getSize() > 0:
            self.currentMediaNode = self.playlist.dummyHead.next
