/**
 * Created by Meital on 2/28/2016.
 */
public class Test {
    public static void main(String[]args){
        Book b = new Book("a", "b", 90, 2,3,4);
        Library l = new Library(3,2,2);
        Patron p = new Patron("aw", "se", 2,3,4,5);
        l.addBookToLibrary(b);
        l.registerPatronToLibrary(p);
        l.borrowBook(0,0);
        System.out.println(b.getCurrentBorrowerId());
        Patron p2 = new Patron("aw", "snmne", 2,3,4,5);
        l.registerPatronToLibrary(p2);
        l.returnBook(0);
        System.out.println(l.isBookAvailable(0));
        l.borrowBook(0,1);
        System.out.println(b.getCurrentBorrowerId());
    }
}
