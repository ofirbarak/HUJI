import java.util.LinkedList;

/**
 * A hash-set based on chaining.
 */
public class OpenHashSet extends SimpleHashSet {
    /* Hash set */
    private WrapperLinkedList[] _hashSet;

    /* -- Methods -- */
    /* Constructors */

    /**
     * A default constructor.
     */
    public OpenHashSet() {
        super(INITIALIZE_CAPACITY, UPPER_LOAD_FACTOR, LOWER_LOAD_FACTOR);
        createEmptyListsInArray();
    }

    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     *
     * @param upperLoadFactor The upper load factor of the hash table.
     * @param lowerLoadFactor The lower load factor of the hash table.
     */
    public OpenHashSet(float upperLoadFactor, float lowerLoadFactor) {
        super(INITIALIZE_CAPACITY, upperLoadFactor, lowerLoadFactor);
        createEmptyListsInArray();
    }

    /**
     * Initialize an array, and create empty lists each cell.
     */
    private void createEmptyListsInArray() {
        _hashSet = new WrapperLinkedList[INITIALIZE_CAPACITY];
        for (int i = 0; i < _hashSet.length; i++)
            _hashSet[i] = new WrapperLinkedList();
    }

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25).
     *
     * @param data Values to add to the set.
     */
    public OpenHashSet(java.lang.String[] data) {
        this();
        for (int i = 0; i < data.length; i++)
            add(data[i]);
    }

    /** Instance Methods */
    /**
     * Add a specified element to the set if it's not already in it.
     *
     * @param newValue New value to add to the set.
     * @return False iff newValue already exists in the set.
     */
    public boolean add(java.lang.String newValue) {
        if (contains(newValue))
            return false;
        _size++;
        if (getLoadFactor() > getUpperLoadFactor())
            reHashing(INCREASE_FACTOR);
        int index = stringIndex(newValue);
        _hashSet[index].add(newValue);
        return true;
    }

    /**
     * Returns the index of a string (in array)
     *
     * @param str string to calculate
     * @return the index of a string (in array)
     */
    private int stringIndex(java.lang.String str) {
        return str.hashCode() & _capacityMinusOne;
    }

    /**
     * Look for a specified value in the set.
     *
     * @param searchVal Value to search for
     * @return True iff searchVal is found in the set
     */
    public boolean contains(String searchVal) {
        return _hashSet[stringIndex(searchVal)].contains(searchVal);
    }

    /**
     * Does a rehashing - increase hash set size by 1, and copy all elements from old to the new one.
     * There is no need to check for duplicates because when we insert values we checked the're not already
     * in the hash set.
     */
    private void reHashing(float factor) {
        // Increase/decrease hash set capacity by 1 power if 2.
        int newSize = Math.round(capacity() * factor);
        if (newSize < 1)
            newSize = 1;
        _capacityMinusOne = newSize - 1;
        WrapperLinkedList[] newHashSet = new WrapperLinkedList[newSize];
        for (int i = 0; i < newSize; i++)
            newHashSet[i] = new WrapperLinkedList();
        // Copy all elements
        for (int i = 0; i < _hashSet.length; i++) {
            LinkedList<String> list = _hashSet[i].getlinkedlist();
            String value;
            for (int index = 0; index < list.size(); index++) {
                value = list.get(index);
                newHashSet[stringIndex(value)].add(value);
            }
        }
        _hashSet = newHashSet;
    }

    /**
     * Remove the input element from the set.
     * @param toDelete Value to delete
     * @return True iff toDelete is found and deleted
     */
    public boolean delete(java.lang.String toDelete) {
        if (!contains(toDelete))
            return false;
        if (!_hashSet[stringIndex(toDelete)].delete(toDelete))
            return false;
        _size--;
        // Check the lower load factor
        if (getLowerLoadFactor() > getLoadFactor())
            reHashing(DECREASE_FACTOR);
        return true;
    }
}

