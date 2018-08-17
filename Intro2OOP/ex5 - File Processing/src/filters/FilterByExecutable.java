package filters;

import exceptions.BadFilterOrderNameException;

import java.io.File;

/**
 * Filter class - files that executable similar to given value.
 */
class FilterByExecutable extends CheckerBoolean implements Filtering{
    private boolean _canExecute;

    FilterByExecutable(String value) throws BadFilterOrderNameException {
        _canExecute = CheckerBoolean.checkValidation(value);
    }

    @Override
    public boolean toFilter(File file) {
        return !file.canExecute() == _canExecute;
    }
}
