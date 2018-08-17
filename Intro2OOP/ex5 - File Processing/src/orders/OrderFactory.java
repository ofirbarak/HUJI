package orders;

import exceptions.BadFilterOrderNameException;
import java.io.File;
import java.util.Comparator;
import java.util.List;

/**
 * Factory class that order files according to the command.
 */
public abstract class OrderFactory{
    /* Commands */
    private static final String ABS = "abs";
    private static final String DEFAULT_ORDER = ABS;
    private static final String SPLIT_CHAR = "#";
    private static final String TYPE = "type";
    private static final String SIZE = "size";
    private static final String REVERSE = "REVERSE";
    private static final String WARNING = "Warning in line ";

    /**
     * Order an array according to a command.
     * @param string the Ordering command.
     * @param files an array to Ordering.
     * @param numberLine the number line in the flt file
     * @return the ordered array.
     */
    public static List<File> orderFiles(String string, List<File> files, int numberLine) {
        SimpleCommand command;
        Comparator<File> simpleOrder;
        try {
            command = parseInput(string);
            switch (command._orderType) {
                case ABS:
                    simpleOrder = CompareByAbs.getInstance();
                    break;
                case TYPE:
                    simpleOrder = CompareByType.getInstance();
                    break;
                case SIZE:
                    simpleOrder = CompareBySize.getInstance();
                    break;
                default:
                    throw new BadFilterOrderNameException();
            }
        } catch (BadFilterOrderNameException e){
            System.err.println(WARNING + Integer.toString(numberLine));
            command = new SimpleCommand();
            simpleOrder = CompareByAbs.getInstance();
        }
        return ReverseOrderDecorator.order(files, simpleOrder, command._toReverse);
    }

    private static SimpleCommand parseInput(String input) throws BadFilterOrderNameException {
        if (input == null)
            return new SimpleCommand();
        String[] strings = input.split(SPLIT_CHAR);
        if (strings.length > 2 || strings.length <= 0)
            throw new BadFilterOrderNameException();
        String command = strings[0];
        boolean toReverse = false;
        if (strings.length == 2) {
            if (strings[1].equals(REVERSE))
                toReverse = true;
            else
                throw new BadFilterOrderNameException();
        }
        return new SimpleCommand(command, toReverse);
    }

    /*
    Nested class - Simple class that represents a input
     */
    private static class SimpleCommand{
        String _orderType;
        boolean _toReverse;

        SimpleCommand(){
            _orderType = DEFAULT_ORDER; // default order
            _toReverse = false;
        }

        SimpleCommand(String orderType, boolean toReverse){
            _orderType = orderType;
            _toReverse = toReverse;
        }
    }
}
