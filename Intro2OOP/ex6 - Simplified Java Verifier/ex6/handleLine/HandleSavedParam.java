package oop.ex6.handleLine;

import oop.ex6.general.GeneralHelpFunctions;
import oop.ex6.handleLine.functions.SJavaFunctionsValidation;
import oop.ex6.scope.FunctionScope;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Handle a saved parameter - variable or function.
 */
public class HandleSavedParam {
    private static final String ASSIGN_VALUE_REGEX = "^\\s*((.+)\\s*=\\s*.+)\\s*;\\s*$";

    /**
     * Checks if line is type of assigning a value to variable, if yes continue in checks. If error occurred
     * throw an exception. If it is not the type line returns false.
     * @param line line to check
     * @return true if passed all checks, false otherwise.
     * @throws Exception
     */
    public static boolean checkAssigningValueToVariable(String line) throws Exception {
        Pattern pattern = Pattern.compile(ASSIGN_VALUE_REGEX);
        Matcher matcher = pattern.matcher(line);
        if (!matcher.find())
            return false;
        return HandleSJavaType.saveOrUpdateVariables(
                ScopeHandler.getVariableType(matcher.group(2).trim()),
                matcher.group(1), true);
    }

    /**
     * Checks if line is the type of calling a method. If yes continue in checks, otherwise returns false.
     * @param line line to checks
     * @return true if passed all checks, false otherwise.
     * @throws Exception
     */
    public static boolean checkAMethodCall(String line) throws Exception {
        String lineWithoutSemicolon = GeneralHelpFunctions.checksAndGetsLineWithoutSemicolon(line);
        FunctionScope functionCall = SJavaFunctionsValidation.checkMethodCall(lineWithoutSemicolon);
        return ScopeHandler.isMethodExists(functionCall);
    }
}

