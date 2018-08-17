package filters;

import java.io.File;

/**
 * Filter class - filter file if it's name contains a string.
 */
class FilterByContains implements Filtering{
    private String _contain;

    FilterByContains(String contain){
        _contain = contain;
    }

    @Override
    public boolean toFilter(File file) {
        return !file.getName().contains(_contain);
    }
}
