package oop.ex6.Exceptions;

/**
 * Bad function params format
 */
public class BadFunctionParamsFormat extends Exception {
    @Override
    public String toString() {
        return "Bad format of function params";
    }
}
