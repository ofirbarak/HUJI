package orders;

import java.io.File;
import java.util.Comparator;

/**
 * Order class - compare by absolute name.
 */
class CompareByAbs implements Comparator<File>{
    private static CompareByAbs compareByAbs = new CompareByAbs();
    private CompareByAbs(){
    }

    static CompareByAbs getInstance(){
        return compareByAbs;
    }

    @Override
    public int compare(File o1, File o2) {
        return o1.getAbsolutePath().compareTo(o2.getAbsolutePath());
    }

}
