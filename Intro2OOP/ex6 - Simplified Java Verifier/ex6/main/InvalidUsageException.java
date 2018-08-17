package oop.ex6.main;

/**
 * Exception for invalid usage in program.
 */
class InvalidUsageException extends Exception {
    @Override
    public String toString() {
        return "Invalid usage";
    }
}
