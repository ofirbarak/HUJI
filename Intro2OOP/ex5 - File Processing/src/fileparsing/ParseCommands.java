package fileparsing;

import exceptions.*;

import java.io.*;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Parse file string to section of filter+order
 */
public abstract class ParseCommands {
    private static final String FILTER = "FILTER";
    private static final String ORDER = "ORDER";

    /**
     * Parse directory to list of files in that related directory.
     * @param directory - directory to parse.
     * @return list of files in directory.
     */
    public static List<File> parseDirectoryToFiles(String directory){
        File folder = new File(directory);
        File[] filesAndDirectories = folder.listFiles();
        List<File> files = new ArrayList<>();
        try {
            for (File filesAndDirectory : filesAndDirectories)
                if (filesAndDirectory.isFile())
                    files.add(filesAndDirectory);
        } catch (NullPointerException e){
        }
        return files;
    }

    /**
     * Parse flt file to sections.
     * @param pathToCommandFile directory to flt file
     * @return list of sections to filter and order to.
     * @throws Exception throws type 2 errors.
     */
    public static List<SimpleSection> parseCommandsToSimpleSections(String pathToCommandFile) throws Exception {
        List<SimpleSection> sections = new ArrayList<>();
        Path path = Paths.get(pathToCommandFile);
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            int numberLineInFile = 1;
            String line = reader.readLine();
            do {
                if (!line.equals(FILTER))
                    throw new BadSectionName(FILTER);
                SimpleSection simpleSection = new SimpleSection();
                int numberLinesInSection = 1;
                boolean isOrderCommandChecked = false;
                while ((line = reader.readLine()) != null && (!line.equals(FILTER) || numberLinesInSection < 3)
                        && numberLinesInSection <= 4) {
                    numberLinesInSection++;
                    if (numberLinesInSection == 2)
                        simpleSection.setFilter(line);
                    if (numberLinesInSection == 3){
                        isOrderCommandChecked = true;
                        checkOrderCommandTypeGood(line);
                    }
                    if (numberLinesInSection == 4)
                        simpleSection.setOrder(line);
                }
                if (simpleSection.getFilter() == null || simpleSection.getFilter().equals(ORDER))
                    throw new SubSectionMissingException(FILTER);
                if (!isOrderCommandChecked)
                    throw new BadSectionName(ORDER);
                simpleSection.setNumberLine(numberLineInFile);
                sections.add(simpleSection);
                numberLineInFile += numberLinesInSection;
            } while ((line ) != null);
        } catch (IOException x) {
            throw new IOFileException();
        } catch (NullPointerException e) {
            throw new BadSectionName(FILTER);
        }
        return sections;
    }

    private static void checkOrderCommandTypeGood(String orderCommand) throws Exception {
        try {
            if (!orderCommand.equals(ORDER))
                throw new BadSectionName(ORDER);
        } catch (NullPointerException e){
            throw new BadSectionName(ORDER);
        }
    }


}
