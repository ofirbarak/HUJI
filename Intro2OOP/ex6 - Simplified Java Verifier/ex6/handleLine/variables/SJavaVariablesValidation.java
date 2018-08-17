package oop.ex6.handleLine.variables;


import oop.ex6.general.GeneralHelpFunctions;
import oop.ex6.handleLine.HandleSJavaType;
import oop.ex6.handleLine.ScopeHandler;
import oop.ex6.scope.SavedParameter;

import java.util.LinkedList;
import java.util.List;

/**
 * Handle a general s-java variables.
 */
public class SJavaVariablesValidation {
    /**
     * Gets a type and the rest of the string, and checks the general pattern- name, value, '=', ';'
     * @param lineWithoutType string of the line excluding the type.
     * @param type type of the variable
     * @throws Exception if pattern is not good
     */
    static List<SavedParameter> checkVariableAssignOrDefinition(String lineWithoutType, String type) throws Exception {
        List<SavedParameter> parametersToSave = new LinkedList<>();
        String[] variables = GeneralHelpFunctions.getSplitParams(lineWithoutType);
        /* Check each variable */
        if (variables != null)
            for (String var : variables)
                parametersToSave.add(getNewParameterToSave(var, type));
        return parametersToSave;
    }

    /*
    Checks the value is in a good format.
     */
    static SavedParameter getNewParameterToSave(String var, String type) throws Exception {
        String[] parts = getNameAndValueInArray(var);
        String name = null, variableValue = null;
        try {
            // Checks if variable is saved in scope
            name = GeneralHelpFunctions.getsAndChecksName(parts[0]);
            SavedParameter savedVariable = ScopeHandler.getVariable(parts[1]);
            if (savedVariable != null) {
                if (ScopeHandler.isAFunctionParameter(savedVariable))
                    checkFunctionParam(type, savedVariable);
                else
                    variableValue = isValueMatchesToAGivenType(type, savedVariable.getValue());
            }
            else
                variableValue = isValueMatchesToAGivenType(type, parts[1]);
        } catch (ArrayIndexOutOfBoundsException e){}
        return new SavedParameter(name, variableValue, type);
    }


    /*
    Check string is format of "<name> = <value>" - there is a name,'=' and value. And returns the parts.
     */
    private static String[] getNameAndValueInArray(String someString) throws Exception {
        String[] parts = someString.split("="); // First cell contains the name and the second the value.
        if (parts.length != 2 && parts.length != 1)
            throw new Exception();
        // Check if value is a name of an existing variable
        parts[0] = parts[0].trim();
        try {
            parts[1] = parts[1].trim();
        }catch (IndexOutOfBoundsException e){}
        return parts;
    }

    private  static void checkFunctionParam(String type, SavedParameter savedParameter) throws Exception {
        // Checking just the type because value is null
        if (!type.equals(savedParameter.getType()))
            throw new Exception();
    }

    /*
    Check value matches the type.
     */
    public static String isValueMatchesToAGivenType(String type, String variableValue) throws Exception {
        if (variableValue == null) // variable value is null
            throw new Exception();
        String varPrimitiveType = getPrimitiveType(variableValue);
        if (type.equals(HandleSJavaType.BOOLEAN)) {
            if (varPrimitiveType.equals(HandleSJavaType.BOOLEAN) ||
                    varPrimitiveType.equals(HandleSJavaType.INT) ||
                    varPrimitiveType.equals(HandleSJavaType.DOUBLE))
                return variableValue;
            throw new Exception();
        }
        if (type.equals(HandleSJavaType.DOUBLE)) {
            if (varPrimitiveType.equals(HandleSJavaType.INT) ||
                    varPrimitiveType.equals(HandleSJavaType.DOUBLE))
                return variableValue;
            throw new Exception();
        }
        if (varPrimitiveType.equals(type))
            return variableValue;
        throw new Exception();
    }

    static String getPrimitiveType(String value){
        String primitiveValue;
        if (value.matches("^-?\\d+$"))
            primitiveValue = HandleSJavaType.INT;
        else if (value.matches("^true|false$"))
            primitiveValue = HandleSJavaType.BOOLEAN;
        else if (value.matches("^-?[0-9]+([.][0-9]+)?$"))
            primitiveValue = HandleSJavaType.DOUBLE;
        else if (value.matches("^'\\S'$"))
            primitiveValue = HandleSJavaType.CHAR;
        else if (value.matches("^\".+\"$"))
            primitiveValue = HandleSJavaType.STRING;
        else
            primitiveValue = null;
        return primitiveValue;
    }
}
