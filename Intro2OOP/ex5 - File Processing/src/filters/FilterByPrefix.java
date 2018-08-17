package filters;

import java.io.File;

/**
 * Filter class - filtering files that starts with a given string.
 */
class FilterByPrefix implements Filtering {
    private String _prefix;

    FilterByPrefix(String prefix){
        _prefix = prefix;
    }

    @Override
    public boolean toFilter(File file) {
        return !(file.getName().indexOf(_prefix) == 0);
    }
}
