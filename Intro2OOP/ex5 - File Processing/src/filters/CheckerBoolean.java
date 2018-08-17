package filters;

import exceptions.BadFilterOrderNameException;

/**
 * Checker class - check the permission is good format.
 */
abstract class CheckerBoolean {
    static boolean checkValidation(String value) throws BadFilterOrderNameException {
        if (value.equals("YES") || value.equals("NO"))
            return value.equals("YES");
        else
            throw new BadFilterOrderNameException();
    }
}
