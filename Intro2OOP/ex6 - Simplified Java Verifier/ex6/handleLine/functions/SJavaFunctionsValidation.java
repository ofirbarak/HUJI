package oop.ex6.handleLine.functions;

import oop.ex6.Exceptions.BadFunctionName;
import oop.ex6.Exceptions.BadFunctionParamsFormat;
import oop.ex6.general.GeneralHelpFunctions;
import oop.ex6.handleLine.ScopeHandler;
import oop.ex6.handleLine.variables.HandleSJavaVariables;
import oop.ex6.scope.FunctionScope;
import oop.ex6.scope.SavedParameter;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * Check S-Java functions.
 */
public class SJavaFunctionsValidation {
    private static final String LINE_IN_PARAMS_FORMAT_REGEX = "^\\s*(\\w[\\w\\d_]*)\\s*[(](.*)\\s*[)]\\s*$";
    private static final String FUNCTION_NAME_NOT_START_WITH_UNDERSCORE_REGEX = "^[a-zA-Z].*$";

    /*
    Gets the method name.
     */
    public static String getName(String line) {
        try {
            return getsNameAndParamsInOnePiece(GeneralHelpFunctions.checksAndGetsLineWithoutOpenBracket(line))[0];
        } catch (Exception e){
            return null;
        }
    }

    /*
    Gets a line and type and validates the function declaration. Returns the new function or null if there
    no function to add.
     */
    public static FunctionScope checkMethodDeclaration(String stringWithoutSuffix) throws Exception {
        String[] nameAndParamsInOnePiece = getsNameAndParamsInOnePiece(stringWithoutSuffix);
        String[] params = GeneralHelpFunctions.getSplitParams(nameAndParamsInOnePiece[1]);
        return new FunctionScope(nameAndParamsInOnePiece[0], checkEachVariableAndReturnsAList(params));
    }

    private static String[] getsNameAndParamsInOnePiece(String stringWithoutSuffix) throws Exception{
        // Check restOfTheString is format of '(<params>)'
        Pattern pattern = Pattern.compile(LINE_IN_PARAMS_FORMAT_REGEX);
        Matcher matcher = pattern.matcher(stringWithoutSuffix);
        if (!matcher.find())
            throw new BadFunctionParamsFormat();
        String[] ret = new String[2];
        ret[0] = GeneralHelpFunctions.getsAndChecksName(matcher.group(1));
        if (!ret[0].matches(FUNCTION_NAME_NOT_START_WITH_UNDERSCORE_REGEX))
            throw new BadFunctionName();
        ret[1] = matcher.group(2);
        return ret;
    }

    private static List<SavedParameter> checkEachVariableAndReturnsAList(String[] params) throws Exception {
        List<SavedParameter> functionParams = new LinkedList<>();
        if (params == null || params[0].equals(""))
            return functionParams;
        for (String var : params){
            if (var.matches("\\s*")) // if variable doesn't exists.
                throw new Exception();
            String[] typeAndName = GeneralHelpFunctions.getsFirstWordAndTheRestOfTheString(var);
            List<SavedParameter> funcParam =
                    HandleSJavaVariables.checkExpressionWithKnowIsFuncParams(
                            typeAndName[1], typeAndName[0], true);
            if (funcParam.size() != 1)
                throw new Exception();
            functionParams.add(funcParam.get(0));
        }
        return functionParams;
    }

    public static FunctionScope checkMethodCall(String lineWithoutSuffix) throws Exception {
        String[] nameAndParamsInOneArray = getsNameAndParamsInOnePiece(lineWithoutSuffix);
        String[] params = GeneralHelpFunctions.getSplitParams(nameAndParamsInOneArray[1]);
        return new FunctionScope(nameAndParamsInOneArray[0],
                checkEachParam(params));
    }

    private static List<SavedParameter> checkEachParam(String[] params) throws Exception {
        if (params.length == 1 && params[0].equals(""))
            return new LinkedList<>();
        List<SavedParameter> functionParams = new LinkedList<>();
        for (String param: params){
            String paramType = HandleSJavaVariables.getPrimitiveType(param);
            if (paramType == null) {
                paramType = ScopeHandler.getVariableType(param);
                param = ScopeHandler.getValue(param);
                if (param == null)
                    throw new Exception();
            }
            functionParams.add(new SavedParameter(null, param, paramType));
        }
        return functionParams;
    }
}
