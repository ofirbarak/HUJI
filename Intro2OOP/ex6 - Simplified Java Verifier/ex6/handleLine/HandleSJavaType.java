package oop.ex6.handleLine;

import oop.ex6.general.GeneralHelpFunctions;
import oop.ex6.handleLine.booleanScope.ConditionStatementHandler;
import oop.ex6.handleLine.functions.SJavaFunctionsValidation;
import oop.ex6.handleLine.variables.HandleSJavaVariables;
import oop.ex6.scope.FunctionScope;
import oop.ex6.scope.Scope;

/**
 * Check if a line opened by a known word is good
 */
public class HandleSJavaType {
    public static final String INT = "int";
    public static final String BOOLEAN = "boolean";
    public static final String FINAL = "final";
    public static final String STRING = "String";
    public static final String DOUBLE = "double";
    public static final String CHAR = "char";
    public static final String VOID = "void";
    public static final String COMMENT_REGEX = "^//.*$";
    public static final String CLOSE_BLOCK_REGEX = "^\\s*}\\s*$";
    public static final String IF = "if";
    public static final String WHILE = "while";
    public static String RETURN_REGEX = "^\\s*return\\s*;\\s*$";

    public static boolean isTypeIsVariable(String type){
        switch (type){
            case INT:
            case DOUBLE:
            case BOOLEAN:
            case STRING:
            case CHAR:
            case FINAL:
                return true;
        }
        return false;
    }

    /**
     * This method will check if a given type is if/while
     * @param type a type of variable
     * @return true iff type is IF/WHILE
     */
    public static boolean isTypeIsSupposeToGenerateNewScope(String type){
        switch (type){
            case IF:
            case WHILE:
                return true;
            default:
                return false;
        }
    }

    /**
     * This method will check if a given string is a Sjava known word.
     * @param type a string represent a word in code.
     * @return true iff the given string is a known word
     */
    public static boolean isAKnownSJavaWord(String type){
        switch (type){
            case INT:
            case DOUBLE:
            case BOOLEAN:
            case STRING:
            case CHAR:
            case FINAL:
            case VOID:
                return true;
            default:
                return false;
        }
    }

    /**
     * Check if line is good format of variable declaration
     * @param type variable(s) type.
     * @param theRestOfTheString the string without declaration type.
     * @return true if succeed in tests. False otherwise.
     * @throws Exception if an error occurred.
     */
    public static boolean checkVariableDeclaration(String type, String theRestOfTheString) throws Exception {
        return saveOrUpdateVariables(type,GeneralHelpFunctions.getStringWithoutSemicolon(theRestOfTheString), false);
    }

    /*
    Add or update new variables, including checking the line.
     */
    static boolean saveOrUpdateVariables(String variableType, String theRestOfTheStringWithoutSemicolon,
                                         boolean toUpdate) throws Exception {
        return ScopeHandler.saveOrUpdateRunningScope(
                HandleSJavaVariables.checkExpression(theRestOfTheStringWithoutSemicolon, variableType),toUpdate);
    }

    /**
     * Gets a line an checks if method declared correctly, otherwise throw an exception.
     * @param type type of the line (just void in our case..)
     * @param string the line without opening
     * @return the new method scope was generated if declaration line passed.
     * @throws Exception if error occurred
     */
    public static Scope checkMethodDeclaration(String type, String string) throws Exception {
        FunctionScope newFunctionToAdd =
                SJavaFunctionsValidation.checkMethodDeclaration(
                        GeneralHelpFunctions.checksAndGetsLineWithoutOpenBracket(string));
        ScopeHandler.addNewMethod(newFunctionToAdd);
        return newFunctionToAdd;
    }

    /**
     * This method will check if/while statements.
     * @param line String represent the rest of line after the if/while declaration
     * @return Scope iff statement is correct
     * @throws Exception if statement isn't valid.
     */
    public static Scope checkIfWhileAndGetsNewScope(String line) throws Exception {
        if (ConditionStatementHandler.extractCondition(
                GeneralHelpFunctions.checksAndGetsLineWithoutOpenBracket(line)))
            return new Scope(ScopeHandler.getScope());
        throw new Exception();
    }
}
