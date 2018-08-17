package filters;

import exceptions.BadFilterOrderNameException;
import filters.filterExceptions.NegativeNumberException;

/**
 * Filter - File size is strictly less than the given number of k-bytes.
 */
class FilterBySmaller extends FilterByFileSize {
    /**
     * Gets a string command and init the parameters.
     * @param command String command
     * @throws NegativeNumberException, BadFilterOrderNameException()
     */
    FilterBySmaller(String command) throws BadFilterOrderNameException, NegativeNumberException {
        String[] splitCommand = command.split("#");
        if (splitCommand.length != 1)
            throw new BadFilterOrderNameException();

        _upperBound = Double.parseDouble(splitCommand[0]);
        if (!(_upperBound >= 0))
            throw new NegativeNumberException();
        _filterByGreater = false;
        _filterBySmaller = true;
    }
}
