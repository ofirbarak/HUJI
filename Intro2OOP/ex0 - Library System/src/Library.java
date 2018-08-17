/**
 * This class represents a library, which hold a collection of books. Patrons can register at the
 *  library to be able to check out books, if a copy of the requested book is available.
 */
public class Library {
    /** The maximal number of books this library allows a single patron to borrow
     * at the same time. */
    final int maxLibraryBorrowedBooks;

    /** Books in the library **/
    Book [] libraryBooks;

    /** The number of current books in library */
    int numOfCurrentBooks;

    /** The patrons in library */
    Patron [] patrons;

    /** The number of patrons in library */
    int numOfPatrons;

   /*----=  Constructors  =-----*/

    /**
     * Creates a new Library with the given characteristic.
     * @param maxBookCapacity - The maximal number of books this library can hold.
     * @param maxBorrowedBooks - The maximal number of books this library allows a single patron to
     *                         borrow at the same time.
     * @param maxPatronCapacity - The maximal number of registered patrons this library can handle.
     */
   Library(int maxBookCapacity, int maxBorrowedBooks, int maxPatronCapacity){
       maxLibraryBorrowedBooks = maxBorrowedBooks;
       libraryBooks = new Book[maxBookCapacity];
       numOfCurrentBooks = 0;
       patrons = new Patron[maxPatronCapacity];
       numOfPatrons = 0;
   }

    /*----=  Instance Methods  =-----*/

    /**
     * Adds the given book to this library, if there is place available, and it isn't already
     * in the library.
     * @param book - The book to add to this library.
     * @return a non-negative id number for the book if there was a spot and the book was
     *  successfully added, or if the book was already in the library; a negative number otherwise.
     */
    int addBookToLibrary(Book book){
        int bookId = getBookId(book);
        if(numOfCurrentBooks < libraryBooks.length &&  bookId == -1) {
            libraryBooks[numOfCurrentBooks] = book;
            book.returnBook();
            numOfCurrentBooks++;
            return numOfCurrentBooks-1;
        }
        return bookId;
    }

    /**
     * Returns true if the given number is an id of some book in the library, false otherwise.
     * @param bookId - The id to check.
     * @return true if the given number is an id of some book in the library, false otherwise.
     */
    boolean isBookIdValid(int bookId){
        if(bookId>=0 && bookId<numOfCurrentBooks)
            return true;
        return false;
    }

    /**
     * Returns the non-negative id number of the given book if he is owned by this library,
     *  -1 otherwise.
     * @param book - The book for which to find the id number.
     * @return a non-negative id number of the given book if he is owned by this library, -1 otherwise.
     */
    int getBookId(Book book){
        for(int i=0; i<numOfCurrentBooks; i++){
            if(book.equals(libraryBooks[i]))
                return i;
        }
        return -1;
    }

    /**
     * Returns true if the book with the given id is available, false otherwise.
     * @param bookId - The id number of the book to check.
     * @return true if the book with the given id is available, false otherwise.
     */
    boolean isBookAvailable(int bookId){
        if(isBookIdValid(bookId) && libraryBooks[bookId].getCurrentBorrowerId() == -1)
            return true;
        return false;
    }

    /**
     * Registers the given Patron to this library, if there is a spot available.
     * @param patron - The patron to register to this library.
     * @return a non-negative id number for the patron if there was a spot and the patron was
     *  successfully registered, a negative number otherwise.
     */
    int registerPatronToLibrary(Patron patron){
        if(numOfPatrons < patrons.length && getPatronId(patron) == -1){
            patrons[numOfPatrons] = patron;
            numOfPatrons++;
            return numOfPatrons-1;
        }
        return -1;
    }

    /**
     * Returns true if the given number is an id of a patron in the library, false otherwise.
     * @param patronId - The id to check.
     * @return true if the given number is an id of a patron in the library, false otherwise.
     */
    boolean isPatronIdValid(int patronId){
        if(patronId >= 0 && patronId < numOfPatrons)
            return true;
        return false;
    }

    /**
     * Returns the non-negative id number of the given patron if he is registered to this library,
     *  -1 otherwise.
     * @param patron - The patron for which to find the id number.
     * @return a non-negative id number of the given patron if he is registered to this library,
     *  -1 otherwise.
     */
    int getPatronId(Patron patron){
        for (int i=0; i < numOfPatrons; i++){
            if(patron.equals(patrons[i]))
                return i;
        }
        return -1;
    }

    /**
     * Marks the book with the given id number as borrowed by the patron with the given patron id,
     *  if this book is available, the given patron isn't already borrowing the maximal number of
     *  books allowed, and if the patron will enjoy this book.
     * @param bookId - The id number of the book to borrow.
     * @param patronId - The id number of the patron that will borrow the book.
     * @return true if the book was borrowed successfully, false otherwise.
     */
    boolean borrowBook(int bookId, int patronId){
        if(!(isBookIdValid(bookId) && isPatronIdValid(patronId)))
            return false;
        if(isBookAvailable(bookId) &&
                returnNumberOfBorrowedBookByPatron(patronId) < maxLibraryBorrowedBooks &&
                patrons[patronId].willEnjoyBook(libraryBooks[bookId])){
            libraryBooks[bookId].setBorrowerId(patronId);
            return true;
        }
        return false;
    }

    /**
     * Help function - Return the number of books that parton has borrowed
     * @param patronId - The id number of the patron to check
     * @return the number of books that parton has borrowed
     */
    int returnNumberOfBorrowedBookByPatron(int patronId){
        int countBorrowedBooks = 0;
        for(int i=0; i<numOfCurrentBooks; i++){
            if(libraryBooks[i].getCurrentBorrowerId() == patronId)
                countBorrowedBooks++;
        }
        return countBorrowedBooks;
    }

    /**
     * Return the given book.
     * @param bookId - The id number of the book to return.
     */
    void returnBook(int bookId){
        if(isBookIdValid(bookId))
            libraryBooks[bookId].returnBook();
    }

    /**
     * Suggest the patron with the given id the book he will enjoy the most, out of all available
     *  books he will enjoy, if any such exist.
     * @param patronId - The id number of the patron to suggest the book to.
     * @return The available book the patron with the given will enjoy the most. Null if no book
     *  is available.
     */
    Book suggestBookToPatron(int patronId){
        Book mostEnjoymentBook = null;
        int mostEnjoymentBookScore = 0;
        if(isPatronIdValid(patronId)) {
            Patron patron = patrons[patronId];
            for (int i = 0; i < numOfCurrentBooks; i++) {
                Book book = libraryBooks[i];
                int bookScore = patron.getBookScore(book);
                if(bookScore > mostEnjoymentBookScore){
                    mostEnjoymentBookScore = bookScore;
                    mostEnjoymentBook = book;
                }
            }
        }
        return mostEnjoymentBook;
    }
}
