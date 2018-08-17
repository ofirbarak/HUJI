package exceptions;

/**
 * Exception for bad section name for filter/order command.
 */
public class BadSectionName extends Exception{
    private String _sectionName;

    public BadSectionName(String name){
        _sectionName = name;
    }

    @Override
    public String toString() {
        return _sectionName + " is an illegal sub-section name";
    }
}
