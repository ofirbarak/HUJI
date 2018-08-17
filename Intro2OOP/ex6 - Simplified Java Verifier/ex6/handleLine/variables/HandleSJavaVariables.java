package oop.ex6.handleLine.variables;

import oop.ex6.handleLine.HandleSJavaType;
import oop.ex6.scope.SavedParameter;
import java.util.LinkedList;
import java.util.List;

/**
 * Check if type is a known s-java variables words.
 */
public class HandleSJavaVariables {
    public static List<SavedParameter> checkExpression(String theRestOfTheString,
                                                       String type)throws Exception{
        return checkExpressionWithKnowIsFuncParams(theRestOfTheString, type, false);
    }

    /**
     * Check if line is: variable declaration, including 'final'
     * @param type variable(s) type.
     * @param theRestOfTheString the string without declaration type.
     * @return true if succeed for recognize a S-Java word. False otherwise.
     * @throws Exception if an error occurred.
     */
    public static List<SavedParameter> checkExpressionWithKnowIsFuncParams(String theRestOfTheString,
                                                                           String type,
                                                                           boolean isFuncParam) throws Exception{
        /* Send checks accordingly the type */
        List<SavedParameter> parametersToSave = null;
        switch (type){
            case HandleSJavaType.FINAL:
                parametersToSave = checkFinalDeclaration(type, theRestOfTheString, isFuncParam);
                break;
            default:
                parametersToSave = checkVariableDeclaration(type, theRestOfTheString, isFuncParam);
                break;
        }
        return parametersToSave;
    }

    /*
    Checks a variable declaration.
     */
    private static List<SavedParameter> checkVariableDeclaration(String variableType,
                                                                 String line,
                                                                 boolean isFunctionParam) throws Exception {
        return SJavaVariablesValidation.checkVariableAssignOrDefinition(line, variableType);
    }

    private static List<SavedParameter> checkFinalDeclaration(String type,
                                                              String line,
                                                              boolean isFuncParam) throws Exception {
        List<SavedParameter> lst = new LinkedList<>();
        SavedParameter parameter =
                SJavaFinalVariableValidation.checkFinalDeclaration(type, line, isFuncParam);
        if (parameter != null)
            lst.add(parameter);
        return lst;
    }

    public static String getPrimitiveType(String param){
        return SJavaVariablesValidation.getPrimitiveType(param.trim());
    }

}
