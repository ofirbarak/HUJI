package orders;

import java.io.File;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * Decorator class, add reverse function to order types.
 * It's abstract class because all functions are relevant for the whole class, we don't create
 * instances from this class.
 */
abstract class ReverseOrderDecorator{

    static List<File> order(List<File> files, Comparator<File> orderType, boolean toReverse) {
        if (files != null && orderType != null) {
            List<File> orderFiles = SimpleOrder.order(files, orderType);
            if (toReverse)
                Collections.reverse(orderFiles);
            return orderFiles;
        }
        return files;
    }
}
