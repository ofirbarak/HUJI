package filters;

import exceptions.BadFilterOrderNameException;
import filters.filterExceptions.IllegalValuesForBetweenFilter;
import filters.filterExceptions.NegativeNumberException;

/**
 * Filter - File size is between (inclusive) the given number of k-bytes.
 */
class FilterBetweenValues extends FilterByFileSize{
    FilterBetweenValues(String command)
            throws NegativeNumberException, BadFilterOrderNameException, IllegalValuesForBetweenFilter {
        String[] splitCommand = command.split("#");
        if (splitCommand.length != 2)
            throw new BadFilterOrderNameException();
        _lowerBound = Double.parseDouble(splitCommand[0]);
        _upperBound = Double.parseDouble(splitCommand[1]);
        _filterByGreater = true;
        _filterBySmaller = true;
        if (_lowerBound > _upperBound)
            throw new IllegalValuesForBetweenFilter();
        if (!(_lowerBound >= 0 && _upperBound >= 0))
            throw new NegativeNumberException();
    }

}
