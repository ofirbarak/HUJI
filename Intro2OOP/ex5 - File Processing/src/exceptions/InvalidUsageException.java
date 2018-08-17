package exceptions;

/**
 * Exception class for Invalid usage.
 */
public class InvalidUsageException extends Exception{
    public InvalidUsageException(){
    }

    @Override
    public String toString() {
        return "Invalid usage";
    }
}
