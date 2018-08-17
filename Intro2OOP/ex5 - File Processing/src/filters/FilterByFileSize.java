package filters;

import java.io.File;

/**
 * Filter - File size.
 */
abstract class FilterByFileSize implements Filtering{
    protected double _lowerBound;
    protected double _upperBound;
    protected boolean _filterByGreater;
    protected boolean _filterBySmaller;

    @Override
    public boolean toFilter(File file) {
        long fileLength = (long) (file.length()/1024.0);
        return  !((fileLength < _upperBound || !_filterBySmaller) &&
                (fileLength > _lowerBound || !_filterByGreater));
    }
}
