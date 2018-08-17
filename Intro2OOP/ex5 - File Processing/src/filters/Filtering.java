package filters;

import java.io.File;

/**
 * Interface for filtering.
 */
interface Filtering {
    /**
     * Decide if to filter a given file.
     * @param file to check.
     * @return true - if that file needs to be extract, false otherwise.
     */
    boolean toFilter(File file);
}
