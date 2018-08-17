import java.util.LinkedList;

/**
 * A class that wrapper the linkedList
 */
public class WrapperLinkedList {
    /* LinkedList of strings */
    private LinkedList<String> _linkedlist;

    /* -- Methods -- */
    /* Constructor */

    /**
     * Initialize a new LinkedList
     */
    public WrapperLinkedList(){
        _linkedlist = new LinkedList<>();
    }

    /**
     * Returns the number of elements in the list
     * @return the number of elements in the list
     */
    public int size() {
        return _linkedlist.size();
    }

    /**
     * Gets a index to insert value in that cell
     * @param newValue
     */
    public void add(String newValue) {
        _linkedlist.add(newValue);
    }

    /**
     * Check if the list contains a given string
     * @param str string to check
     * @return true if yes, other false
     */
    public boolean contains(String str){
        return _linkedlist.contains(str);
    }

    public LinkedList<String> getlinkedlist(){
        return _linkedlist;
    }

    public boolean delete(String toDelete){
        return _linkedlist.remove(toDelete);
    }
}
