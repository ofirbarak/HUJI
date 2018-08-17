package oop.ex6.Exceptions;

/**
 * Missing semicolon at the end of the line
 */
public class NoSemicolonAtEndsOfTheLine extends Exception {
    @Override
    public String toString() {
        return "Missing semicolon";
    }
}
