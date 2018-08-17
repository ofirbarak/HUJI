package exceptions;

/**
 * Error occurred in accessing commands file.
 */
public class IOFileException extends Exception{
    public IOFileException(){
        super();
    }

    @Override
    public String toString() {
        return "Can not accessing command file\n";
    }
}
