package oop.ex6.handleLine.booleanScope;

import oop.ex6.handleLine.HandleSJavaType;
import oop.ex6.handleLine.ScopeHandler;
import oop.ex6.handleLine.variables.SJavaVariablesValidation;
import oop.ex6.scope.SavedParameter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * a class which handle all if/while statements
 */
public class ConditionStatementHandler {

    final static String CONDITION_STATEMENT_EXTRACT_REGEX = "^\\s*[(]\\s*(.*)\\s*[)]\\s*$";
    final static String CONDITION_STATEMENT_REGEX = " ";
    final static String TRUE_RESERVED = "true";
    final static String FALSE_RESERVED = "false";
    final static String OR_OPERATOR = "||";
    final static String AND_OPERATOR = "&&";


    /**
     * This method will extract the given condition from the restOfString.
     * This method will be called only when parser met a if/while.
     * @param restOfString the string we need to extract condition from.
     * @return true false if there is not valid condition.
     */
    public static boolean extractCondition(String restOfString) {
        Pattern extractIfCondition = Pattern.compile(CONDITION_STATEMENT_EXTRACT_REGEX);
        Matcher matcher = extractIfCondition.matcher(restOfString);
        String ifCondition;
        if (matcher.find()) {
            ifCondition = matcher.group(1);
            return examineCondition(ifCondition);
        } else
            return false;
    }

    /**
     * This method examines the condition statement.
     * @param conditionStatement a string we received from extractCondition method.
     * @return false if the condition isn't valid one.
     */
    public static boolean examineCondition(String conditionStatement) {
        boolean validCondition = false;
        String[] conditionStatementBlocks = conditionStatement.split(CONDITION_STATEMENT_REGEX);
        for (int i=0; i<conditionStatementBlocks.length; i++) {
            switch (conditionStatementBlocks[i]) {
                case TRUE_RESERVED:
                    validCondition = true;
                    break;
                case FALSE_RESERVED:
                    validCondition = true;
                    break;
                case OR_OPERATOR:
                    validCondition = checkOrAndOperatorsValidity(conditionStatementBlocks, i);
                    break;
                case AND_OPERATOR:
                    validCondition = checkOrAndOperatorsValidity(conditionStatementBlocks, i);
                    break;
                default:
                    validCondition = checkOtherBooleanTypes(conditionStatementBlocks[i]);
                    break;
            }
            if (!validCondition)
                break;
        }
        return validCondition;
    }

    /**
     *
     * @param conditionStatementBlocks a string[] contains all the words in the condition.
     * @param index the index of the operator in the condition statement.
     * @return false if operator isn't valid
     */
    static boolean checkOrAndOperatorsValidity(String[] conditionStatementBlocks, int index) {
        //if operator located at odd index that indicates that there is no boolean variable after
        // the operator/
        // there first word in the condition is operator.
        if (index % 2 != 1)
            return false;
        try {
            switch (conditionStatementBlocks[index + 1]) { // check the next word at the statement.
                case OR_OPERATOR:
                    return false;
                case AND_OPERATOR:
                    return false;
                default:
                    return true;
            }
        }catch (NullPointerException nullError) {
            return false;
        }
    }

    /**
     * This method will check all other boolean types but operators.
     * @param conditionStatement a string we received from extractCondition method.
     * @return false if the condition isn't valid one.
     */
    static boolean checkOtherBooleanTypes(String conditionStatement) {
        SavedParameter currentVarToCheck = ScopeHandler.getVariable(conditionStatement);
        try {
            switch (currentVarToCheck.getType()) {
                case HandleSJavaType.BOOLEAN:
                case HandleSJavaType.DOUBLE:
                case HandleSJavaType.INT:
                    return (currentVarToCheck.getValue() != null);
            }
        } catch (NullPointerException nullError) {
            try {
                if (SJavaVariablesValidation.isValueMatchesToAGivenType(HandleSJavaType.BOOLEAN,
                        conditionStatement) != null) {
                    return true;
                }
            } catch (Exception e) {
                return false;
            }
        }
        return false;
    }
}
