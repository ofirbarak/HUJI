package filters;

import exceptions.BadFilterOrderNameException;

import java.io.File;

/**
 * Filter class - filter files are hidden.
 */
class FilterByHidden implements Filtering{
    private boolean _isHidden;

    FilterByHidden(String value) throws BadFilterOrderNameException {
        _isHidden = CheckerBoolean.checkValidation(value);
    }

    @Override
    public boolean toFilter(File file) {
        return !file.isHidden() == _isHidden;
    }
}
