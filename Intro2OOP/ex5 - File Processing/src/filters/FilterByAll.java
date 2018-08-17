package filters;

import exceptions.BadFilterOrderNameException;

import java.io.File;

/**
 * Filter - "all files are matched"
 */
class FilterByAll implements Filtering {
    FilterByAll(){}

    FilterByAll(String command) throws BadFilterOrderNameException {
        String[] splitCommand = command.split("#");
        if (splitCommand.length != 1)
            throw new BadFilterOrderNameException();
    }

    @Override
    public boolean toFilter(File file) {
        return false;
    }
}
