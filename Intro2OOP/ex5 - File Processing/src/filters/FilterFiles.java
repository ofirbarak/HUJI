package filters;

import java.io.File;
import java.util.Iterator;
import java.util.List;

/**
 * Filter files according to a given filter.
 */
class FilterFiles {
    private NotFilterDecorator _notFilterDecorator;
    private Filtering _filter;

    FilterFiles(boolean isNot, Filtering filter){
        _notFilterDecorator = new NotFilterDecorator(isNot);
        _filter = filter;
    }

    List<File> filter(List<File> files) {
        for (Iterator<File> iterator = files.iterator(); iterator.hasNext(); ) {
            File file = iterator.next();
            if (_notFilterDecorator.getResult(_filter.toFilter(file)))
                iterator.remove();
        }
        return files;
    }
}
