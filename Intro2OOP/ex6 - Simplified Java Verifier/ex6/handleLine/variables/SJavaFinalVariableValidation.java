package oop.ex6.handleLine.variables;

import oop.ex6.scope.SavedParameter;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Checks for final. That's a class for adding more modifiers (just change the parameter in the function
 * 'setModifier'.
 */
class SJavaFinalVariableValidation extends SJavaVariablesValidation {
    static SavedParameter checkFinalDeclaration(String modifier,
                                                       String lineWithoutSemicolon,
                                                       boolean isFuncPram) throws Exception {
        Pattern pattern = Pattern.compile("^\\s*(\\w+)\\s*(.*)$");
        Matcher matcher = pattern.matcher(lineWithoutSemicolon);
        if (!matcher.matches())
            throw new Exception();
        String type = matcher.group(1);
        String nameAndValue = matcher.group(2);
        SavedParameter parameter = getNewParameterToSave(nameAndValue, type);
        if (!isFuncPram && parameter.getValue() == null)
            throw new Exception();
        parameter.setModifier(modifier);
        return parameter;
    }
}
