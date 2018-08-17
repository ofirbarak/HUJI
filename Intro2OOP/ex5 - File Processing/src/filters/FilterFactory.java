package filters;

import exceptions.BadFilterOrderNameException;
import filters.filterExceptions.IllegalValuesForBetweenFilter;
import filters.filterExceptions.NegativeNumberException;

import java.io.File;
import java.util.List;

/**
 * Class that filter an array of file according to a command.
 */
public abstract class FilterFactory {
    /* Commands */
    private static final String BETWEEN_COMMAND = "between";
    private static final String GREATER_COMMAND = "greater_than";
    private static final String SMALLER_COMMAND = "smaller_than";
    private static final String ALL_COMMAND = "all";
    private static final String FILE_COMMAND = "file";
    private static final String CONTAINS_COMMAND = "contains";
    private static final String PREFIX_COMMAND = "prefix";
    private static final String SUFFIX_COMMAND = "suffix";
    private static final String WRITABLE_COMMAND = "writable";
    private static final String EXECUTABLE_COMMAND = "executable";
    private static final String HIDDEN_COMMAND = "hidden";
    private static final String NOT = "NOT";
    private static final String WARNING = "Warning in line ";
    private static final String DEFAULT_COMMAND = ALL_COMMAND;

    /**
     * Filter an array according to a command.
     * @param stringFilters the filtering command.
     * @param files an array to filtering.
     * @param numberLine number line in the flt file.
     * @return the filtering array.
     */
    public static List<File> filterFiles(String stringFilters, List<File> files, int numberLine) {
        Filtering someFilter;
        SimpleSplitterCommand splitCommand = parseInput(stringFilters);
        try {
            switch (splitCommand._command){
                case BETWEEN_COMMAND:
                    someFilter = new FilterBetweenValues(splitCommand._arguments);
                    break;
                case GREATER_COMMAND:
                    someFilter = new FilterByGreater(splitCommand._arguments);
                    break;
                case SMALLER_COMMAND:
                    someFilter = new FilterBySmaller(splitCommand._arguments);
                    break;
                case ALL_COMMAND:
                    someFilter = new FilterByAll(splitCommand._arguments);
                    break;
                case FILE_COMMAND:
                    someFilter = new FilterByEqualsToValue(splitCommand._arguments);
                    break;
                case CONTAINS_COMMAND:
                    someFilter = new FilterByContains(splitCommand._arguments);
                    break;
                case PREFIX_COMMAND:
                    someFilter = new FilterByPrefix(splitCommand._arguments);
                    break;
                case SUFFIX_COMMAND:
                    someFilter = new FilterBySuffix(splitCommand._arguments);
                    break;
                case WRITABLE_COMMAND:
                    someFilter = new FilterByWritable(splitCommand._arguments);
                    break;
                case EXECUTABLE_COMMAND:
                    someFilter = new FilterByExecutable(splitCommand._arguments);
                    break;
                case HIDDEN_COMMAND:
                    someFilter = new FilterByHidden(splitCommand._arguments);
                    break;
                default:
                    System.err.println(WARNING + Integer.toString(numberLine));
                    someFilter = new FilterByAll();
                    break;
            }
        } catch (BadFilterOrderNameException | NegativeNumberException | IllegalValuesForBetweenFilter e){
            System.err.println(WARNING + Integer.toString(numberLine));
            someFilter = new FilterByAll(); // Default filter
            splitCommand = new SimpleSplitterCommand();
        }
        FilterFiles filterFiles = new FilterFiles(splitCommand._isNotFiltering, someFilter);
        return filterFiles.filter(files);
    }

    private static SimpleSplitterCommand parseInput(String input) {
        if (input == null)
            return new SimpleSplitterCommand();
        String[] strings = input.split("#");
        if (strings.length <= 0)
            return new SimpleSplitterCommand();
        SimpleSplitterCommand simpleSplitterCommand = new SimpleSplitterCommand();
        if (strings.length >= 1)
            simpleSplitterCommand._command = strings[0];
        int end = input.length();
        if (strings[strings.length - 1].equals(NOT)) {
            simpleSplitterCommand._isNotFiltering = true;
            end -= 4;
        }
        try {
            simpleSplitterCommand._arguments = input.substring(strings[0].length() + 1, end);
        } catch (StringIndexOutOfBoundsException e){}
        return simpleSplitterCommand;
    }

    private static class SimpleSplitterCommand{
        String _command;
        String _arguments;
        boolean _isNotFiltering;

        SimpleSplitterCommand(){
            _command = DEFAULT_COMMAND;
            _arguments = "";
            _isNotFiltering = false;
        }
    }
}
