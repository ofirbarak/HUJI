package oop.ex6.scope;

import java.util.*;

/**
 * Represents a function scope.
 */
public class FunctionScope extends Scope {
    private String _functionName;
    private List<SavedParameter> _parameters;

    /**
     * Generate a new function scope.
     * @param functionName function name
     * @param params params of function, null if there isn't.
     */
    public FunctionScope(String functionName, List<SavedParameter> params) {
        _functionName = functionName;
        _parameters = new LinkedList<>();
        for (SavedParameter parameter: params)
            _parameters.add(parameter);
    }

    /**
     * Check if params of given function are fitting to this
     * @param function2 function to check
     * @return true if yes, false otherwise
     */
    public boolean areParamsFitting(FunctionScope function2){
        Collection<SavedParameter> function2Params = function2._parameters;
        if (_parameters.size() != function2Params.size())
            return false;
        Iterator<SavedParameter> it2 = function2Params.iterator();
        Iterator<SavedParameter> it1 = _parameters.iterator();
        while (it1.hasNext() && it2.hasNext()) {
            SavedParameter param2 = it2.next();
            if (!it1.next().equals(param2) && param2.getValue() != null)
                return false;
        }
        return true;
    }

    /**
     * Adds function params to variables
     * @throws Exception
     */
    public void updateMethodValues() throws Exception {
        for (int i = 0; i < _parameters.size(); i++) {
            SavedParameter s = _parameters.get(i);
            if (_variables.containsKey(s.getName()))
                throw new Exception();
            _variables.put(s.getName(), s);
        }
    }

    /**
     * Check if given savedParameter is this  function param.
     * @param savedParameter param to check
     * @return true if yes, false otherwise
     */
    public boolean isAFunctionParam(SavedParameter savedParameter){
        for (SavedParameter param: _parameters)
            if (param.getName().equals(savedParameter.getName()) && param.equals(savedParameter))
                return true;
        return false;
    }

    public String getFunctionName(){
        return _functionName;
    }

    /**
     * Checks if a variable is exists in variables or in function params
     * @param variable variable name to check.
     * @return true if yes, false otherwise
     */
    @Override
    public boolean isVariableExists(String variable){
        if (super.isVariableExists(variable) || _parameters.contains(variable))
            return true;
        return false;
    }
}
