package filters;

import java.io.File;

/**
 * Filter class - filter files that ends with a given suffix.
 */
class FilterBySuffix implements Filtering{
    private String _suffix;

    FilterBySuffix(String suffix){
        _suffix = suffix;
    }

    @Override
    public boolean toFilter(File file) {
        return !file.getName().endsWith(_suffix);
    }
}
