package orders;

import java.io.File;
import java.util.Comparator;

/**
 * Order class - compare by file type.
 */
class CompareByType implements Comparator<File>{
    private static CompareByType compareByType = new CompareByType();

    private CompareByType(){
    }

    static CompareByType getInstance(){
        return compareByType;
    }

    @Override
    public int compare(File o1, File o2) {
        String o1Extension = getFileExtension(o1);
        String o2Extension = getFileExtension(o2);
        if (o1Extension.equals(o2Extension))
            return CompareByAbs.getInstance().compare(o1, o2);
        return o1Extension.compareTo(o2Extension);
    }

    private String getFileExtension(File file) {
        String fileName = file.getName();
        if(fileName.lastIndexOf(".") != -1 && fileName.lastIndexOf(".") != 0) {
            int end = fileName.length();
            if (fileName.charAt(end-1) == '.')
                end--;
            return fileName.substring(fileName.lastIndexOf(".") + 1, end);
        }
        else return "";
    }
}
