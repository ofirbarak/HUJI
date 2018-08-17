package orders;

import java.io.File;
import java.util.Comparator;

/**
 * Order class - compare by file size.
 */
class CompareBySize implements Comparator<File>{
    private static CompareBySize compareBySize = new CompareBySize();
    private CompareBySize(){
    }

    static CompareBySize getInstance(){
        return compareBySize;
    }

    @Override
    public int compare(File o1, File o2) {
        if (o1.length() == o2.length())
            return CompareByAbs.getInstance().compare(o1, o2);
        return java.lang.Long.compare(o1.length(), o2.length());
    }

}
