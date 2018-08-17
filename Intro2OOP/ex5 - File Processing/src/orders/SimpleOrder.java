package orders;

import java.io.File;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * Class that order files according to a given comparator.
 */
abstract class SimpleOrder{
    static List<File> order(List<File> files, Comparator<File> comparator){
        Collections.sort(files, comparator);
        return files;
    }
}
