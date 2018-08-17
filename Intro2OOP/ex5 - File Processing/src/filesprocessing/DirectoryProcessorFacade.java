package filesprocessing;

import exceptions.InvalidUsageException;
import fileparsing.ParseCommands;
import fileparsing.SimpleSection;
import filters.FilterFactory;
import orders.OrderFactory;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * Facade class - give more simpler usage in the program for users.
 */
class DirectoryProcessorFacade {
    List<File> files;
    List<SimpleSection> sections;
    DirectoryProcessorFacade(String[] args) throws Exception {
        if (args.length != 2)
            throw new InvalidUsageException();
        String sourcedir = args[0];
        String commandfile = args[1];
        files = ParseCommands.parseDirectoryToFiles(sourcedir);
        sections = ParseCommands.parseCommandsToSimpleSections(commandfile);
    }

    void run() {
        for (SimpleSection simpleSection: sections){
            List<File> filteredFiles;
            List<File> orderedFiles;
            filteredFiles = FilterFactory.filterFiles(simpleSection.getFilter(), new ArrayList<>(files),
                    simpleSection.getNumberLine()+1);
            orderedFiles = OrderFactory.orderFiles(simpleSection.getOrder(), filteredFiles,
                    simpleSection.getNumberLine()+3);
            printFilesNames(orderedFiles);
        }
    }

    private void printFilesNames(List<File> files){
        for (File file : files) {
            System.out.println(file.getName());
        }
    }
}
