

/**
 * A hash-set based on closed-hashing with quadratic probing. Extends SimpleHashSet.
 */
public class ClosedHashSet extends SimpleHashSet{
    /* Hash set */
    private String[] _hashSet;

    private final String DELETED = new String("deleted");

    /* -- Methods -- */
    /* Constructors */

    /**
     * A default constructor. Constructs a new, empty table with default initial capacity (16), upper load
     * factor (0.75) and lower load factor (0.25).
     */
    public ClosedHashSet(){
        super(INITIALIZE_CAPACITY, UPPER_LOAD_FACTOR, LOWER_LOAD_FACTOR);
        _hashSet = new String[INITIALIZE_CAPACITY];
    }

    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     * @param upperLoadFactor The upper load factor of the hash table.
     * @param lowerLoadFactor The lower load factor of the hash table.
     */
    public ClosedHashSet(float upperLoadFactor, float lowerLoadFactor){
        super(INITIALIZE_CAPACITY, upperLoadFactor, lowerLoadFactor);
        _hashSet = new String[INITIALIZE_CAPACITY];
    }

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25).
     * @param data Values to add to the set.
     */
    public ClosedHashSet(java.lang.String[] data){
        this();
        for (int i=0; i < data.length; i++)
            add(data[i]);
    }

    private ClosedHashSet(int capacity, float upperLoadFactor, float lowerLoadFactor){
        super(capacity, upperLoadFactor, lowerLoadFactor);
        _hashSet = new String[capacity];
    }
    /**
     * Description copied from interface: supplied.SimpleSet
     * Add a specified element to the set if it's not already in it.
     * @param newValue New value to add to the set
     * @return False iff newValue already exists in the set
     */
    public boolean add(String newValue){
        int i = 0;
        int index;
        int indexToValue = -1;
        String arrValue;
        do {
            index = getNextIndexValue(i, newValue);
            arrValue = _hashSet[index];
            if (arrValue != null && arrValue.equals(newValue))
                return false;
            if (indexToValue == -1 && (arrValue == null || arrValue == DELETED))
                indexToValue = index;
            i++;
        } while (arrValue != null && i < capacity());
        _hashSet[indexToValue] = newValue;
        _size++;
        if (getUpperLoadFactor() < getLoadFactor())
            reHashing(INCREASE_FACTOR);
        return true;
    }

    /**
     * Find the index from a with given values
     * @param i represents the i'th try
     * @param value string to be hash
     * @return index number
     */
    private int getNextIndexValue(int i, String value){
        return value.hashCode() + ((i+ i*i)/2)&(_capacityMinusOne);
    }

    public boolean contains(java.lang.String searchVal){
        int i = 0;
        int index;
        String arrValue;
        do {
            index = getNextIndexValue(i, searchVal);
            arrValue = _hashSet[index];
            if (arrValue != null && arrValue.equals(searchVal))
                return true;
            i++;
        } while (arrValue != null && i < capacity());
        return false;
    }

    public boolean delete(java.lang.String toDelete){
        int i = 0;
        int index;
        String arrValue;
        do {
            index = getNextIndexValue(i, toDelete);
            arrValue = _hashSet[index];
            if (arrValue != null && arrValue.equals(toDelete)) {
                _hashSet[index] = DELETED; // Mark as deleted - Solution in O(1)
                _size--;
                if (getLowerLoadFactor() > getLoadFactor())
                    reHashing(DECREASE_FACTOR);
                return true;
            }
            i++;
        } while (arrValue != null && i < capacity());
        return false;
    }

    /**
     * Does a rehashing - increase hash set size by 1, and copy all elements from old to the new one.
     * There is no need to check for duplicates because when we insert values we checked the're not already
     * in the hash set.
     */
    private void reHashing(float factor) {
        // Increase/decrease hash set capacity by 1 power if 2.
        int newSize = Math.round(capacity()*factor);
        if (newSize < 1)
            newSize = 1;
        _capacityMinusOne = newSize-1;
        ClosedHashSet newHashSet = new ClosedHashSet(newSize, getUpperLoadFactor(), getLowerLoadFactor());
        // Copy all elements
        for (int i=0; i < _hashSet.length; i++){
            String c = _hashSet[i];
            if (_hashSet[i] != null &&_hashSet[i] != DELETED)
                newHashSet.add(_hashSet[i]);
        }
        _hashSet = newHashSet._hashSet;
    }
}
