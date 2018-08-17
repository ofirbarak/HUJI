package exceptions;

/**
 * Error in subsection is missing - filter/order.
 */
public class SubSectionMissingException extends Exception{
    private String _msg;

    public SubSectionMissingException(String section) {
        _msg = section;
    }

    @Override
    public String toString() {
        return "no " +_msg + " sub-section missing\n";
    }
}
