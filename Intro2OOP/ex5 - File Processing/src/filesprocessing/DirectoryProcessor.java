package filesprocessing;

/**
 * Main class - contains the main method.
 */
public class DirectoryProcessor {
    public static void main(String[] args){
        try {
            DirectoryProcessorFacade program = new DirectoryProcessorFacade(args);
            program.run();
        } catch (Exception e){
            System.err.println("ERROR: " + e.toString());
        }
    }
}
