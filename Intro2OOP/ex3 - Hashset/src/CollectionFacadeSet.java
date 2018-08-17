/**
 * Wraps an underlying Collection and serves to both simplify its API and give it a common type
 * with the implemented SimpleHashSets.
 */
public class CollectionFacadeSet extends java.lang.Object implements SimpleSet {

    /* Collection */
    protected java.util.Collection<java.lang.String> _collection;

    /**
     * Creates a new facade wrapping the specified collection.
     * @param collection The Collection to wrap.
     */
    public CollectionFacadeSet(java.util.Collection<java.lang.String> collection){
        _collection = collection;
    }

    public boolean add(java.lang.String newValue){
        if (!contains(newValue))
            return  _collection.add(newValue);
        return false;
    }

    public boolean contains(String searchVal){
        return _collection.contains(searchVal);
    }

    public boolean delete(String toDelete){
        return _collection.remove(toDelete);
    }

    public int size() {
        return _collection.size();
    }
}
