package oop.ex6.main;

import java.io.FileInputStream;
import java.io.IOException;

/**
 * Main class.
 */
public class Sjavac {
    public static void main(String[] args){
        Parser.resetParser();
        try {
            if (args.length != 1)
                throw new InvalidUsageException();
            FileInputStream flt = new FileInputStream(args[0]);
            Parser.run(flt, args[0]);
            System.out.println(0);
        } catch (IOException e){
            System.out.println(2);
            System.err.println(e.toString());
        } catch (Exception e){
            System.out.println(1);
            System.err.println(e.toString());
        }
    }
}
