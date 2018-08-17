package filters;

import exceptions.BadFilterOrderNameException;

import java.io.File;

/**
 * Filter class - filter files are writable.
 */
class FilterByWritable implements Filtering{
    private boolean _writable;

    FilterByWritable(String value) throws BadFilterOrderNameException {
        _writable = CheckerBoolean.checkValidation(value);
    }

    @Override
    public boolean toFilter(File file) {
        return !file.canWrite() == _writable;
    }
}
