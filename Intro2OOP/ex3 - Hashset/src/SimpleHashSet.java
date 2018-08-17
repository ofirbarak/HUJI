/**
 * An abstract class implementing SimpleSet.
 */
public abstract class SimpleHashSet implements SimpleSet{
    /* Constants */
    protected static float UPPER_LOAD_FACTOR = 0.75f;
    protected static float LOWER_LOAD_FACTOR = 0.25f;
    protected static int INITIALIZE_CAPACITY = 16;
    protected static float DECREASE_FACTOR = 0.5f;
    protected static float INCREASE_FACTOR = 2f;

    /* Capacity - 1 */
    protected int _capacityMinusOne;

    /* Upper load factor */
    private float _upperLoadFactor;

    /* Lower load factor */
    private float _lowerLoadFactor;

    /* Set size */
    protected int _size;

    /* -- Methods -- */
    /* Constructor */
    /**
     * Creates an array of linked list
     * @param capacity array size
     * @param upperLoadFactor how fully the table is allowed to get before its capacity is increased
     *                        respectively.
     * @param lowerLoadFactor how empty the table is allowed to get before its capacity is decreased
     *                        respectively.
     */
    public SimpleHashSet(int capacity, float upperLoadFactor, float lowerLoadFactor){
        _upperLoadFactor = upperLoadFactor;
        _lowerLoadFactor = lowerLoadFactor;
        _capacityMinusOne = capacity-1;
        _size = 0;
    }

    /**
     * Returns upper load factor
     * @return upper load factor
     */
    protected float getUpperLoadFactor(){
        return _upperLoadFactor;
    }

    /**
     * Returns lower load factor
     * @return lower load factor
     */
    protected float getLowerLoadFactor(){
        return _lowerLoadFactor;
    }

    /**
     * Returns the load factor of hash table
     * @return the load factor of hash table
     */
    protected double getLoadFactor(){
        return (float)size()/(float)capacity();
    }

    public int capacity(){
        return _capacityMinusOne+1;
    }

    public abstract boolean add(String newValue);

    public abstract boolean contains(String searchVal);

    public abstract boolean delete(String toDelete);

    public int size(){
        return _size;
    }
}
