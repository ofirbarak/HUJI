package oop.ex6.handleLine;

import oop.ex6.scope.FunctionScope;
import oop.ex6.scope.MainScope;
import oop.ex6.scope.SavedParameter;
import oop.ex6.scope.Scope;
import java.util.List;

/**
 * Handle scope functions.
 */
public class ScopeHandler {
    private static Scope _scope;
    public static String _nameOfLastLine;

    public static void resetScopeHandler(){
        _nameOfLastLine = null;
    }

    public static void updateScope(Scope newScope){
        _scope = newScope;
    }

    public static Scope getScope(){
        return _scope;
    }

    static boolean saveOrUpdateRunningScope(List<SavedParameter> parametersToSave,
                                       boolean toUpdate) throws Exception {
        if (parametersToSave != null) {
            for(SavedParameter param: parametersToSave)
                if (toUpdate)
                    updateVariableValue(param);
                else
                    addNewVariable(param);
            return true;
        }
        else
            return false;
    }

    private static void addNewVariable(SavedParameter parameterToSave) throws Exception {
        if (_scope.isVariableExists(parameterToSave.getName()))
            throw new Exception();
        _scope.addVariable(parameterToSave);
    }

    private static void updateVariableValue(SavedParameter parameter) throws Exception {
        if (MainScope.getInstance().isVariableExists(parameter.getName())) {
            _scope.updateVariable(parameter);
            return;
        }
        if (_scope instanceof FunctionScope){
            if (((FunctionScope) _scope).isAFunctionParam(parameter))
                if (parameter.getValue() != null) {
                    _scope.updateVariable(parameter);
                    return;
                }
        }
        SavedParameter exist = _scope.getVariable(parameter.getName());
        if (exist != null) {
            if (exist.getValue() == null) {
                if ((_nameOfLastLine != null && _nameOfLastLine.equals(parameter.getName()))) {
                    _scope.updateVariable(parameter);
                    return;
                }
            } else {
                _scope.updateVariable(parameter);
                return;
            }
        }
        throw new Exception();
    }

    /*
    Check that a given variable is defined, and if yes returns the value, if not returns null.
    If variable value is null throw an exception.
     */
    public static String getValue(String variableName) throws Exception {
        try {
            SavedParameter s = _scope.getVariable(variableName);
            if (s.getValue() == null)
                throw new Exception();
            return s.getValue();
        }catch (NullPointerException e){
            return null;
        }
    }

    public static SavedParameter getVariable(String variableName){
        try {
            return _scope.getVariable(variableName);
        }catch (NullPointerException e){
            return null;
        }
    }

    public static boolean isAFunctionParameter(SavedParameter s){
        if (_scope instanceof FunctionScope)
            return ((FunctionScope) _scope).isAFunctionParam(s);
        return false;
    }

    public static String getVariableType(String variable){
        try {
            return _scope.getVariable(variable).getType();
        } catch (NullPointerException e){
            return null;
        }
    }

    // --------------------------- Methods -------------------------------------------------

    static void addNewMethod(FunctionScope newFunction) throws Exception {
        if (_scope instanceof MainScope) {
            newFunction.setParentScope(_scope);
            ((MainScope) _scope).addFunction(newFunction);
        }
        else
            throw new Exception();
    }

    static boolean isMethodExists(FunctionScope function){
        return (MainScope.getInstance()).isMethodExists(function);
    }
}
