package filters;

import java.io.File;

/**
 * Filter class - filter by name equals to some value.
 */
class FilterByEqualsToValue implements Filtering{
    private String _value;

    FilterByEqualsToValue(String value){
        _value = value;
    }

    @Override
    public boolean toFilter(File file) {
        return !file.getName().equals(_value);
    }
}
