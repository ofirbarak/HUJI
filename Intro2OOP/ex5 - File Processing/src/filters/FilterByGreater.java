package filters;

import exceptions.BadFilterOrderNameException;
import filters.filterExceptions.NegativeNumberException;

/**
 * Filter - File size is strictly greater than the given number of k-bytes.
 */
class FilterByGreater extends FilterByFileSize {
    /**
     * Gets a string command and init the parameters.
     * @param command String command
     * @throws BadFilterOrderNameException, NegativeNumberException
     */
    FilterByGreater(String command) throws BadFilterOrderNameException, NegativeNumberException {
        String[] splitCommand = command.split("#");
        if (splitCommand.length != 1)
            throw new BadFilterOrderNameException();

        _lowerBound = Double.parseDouble(splitCommand[0]);
        if (!(_lowerBound >= 0))
            throw new NegativeNumberException();
        _filterByGreater = true;
        _filterBySmaller = false;
    }
}
