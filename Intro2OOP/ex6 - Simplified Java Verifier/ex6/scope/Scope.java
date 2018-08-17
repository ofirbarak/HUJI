package oop.ex6.scope;

import java.util.HashMap;
import java.util.Map;

/**
 * Class that represents a scope in the file.
 */
public class Scope {
    protected Scope _parentScope; // Parent scope.
    protected int _numberOfOpenBracket = 1;
    protected int _numberOfCloseBracket = 0;

    /* HashMap ( handle a big data quickly), variables in this scope1 */
    protected Map<String, SavedParameter> _variables;
    /* Represents external variables that have been changed */
    protected Map<String, SavedParameter> _externalVariables;

    /**
     * Generate a new simple scope. With default parameters.
     */
    public Scope() {
        _parentScope = null;
        _variables = new HashMap<>();
        _externalVariables = new HashMap<>();
    }

    /**
     * Generate a simple scope with a given parent scope.
     * @param parentScope parent scope
     */
    public Scope(Scope parentScope) {
        this();
        _parentScope = parentScope;
    }

    /*
    Returns parent scope.
     */
    public Scope getParentScope(){
        return _parentScope;
    }

    /*
    Check if scope was ended (occurred when number of open bracket and closed are equal.
     */
    public boolean isScopeEnded(){
        return _numberOfOpenBracket <= _numberOfCloseBracket;
    }

    /*
    Increase number of open brackets.
     */
    public void increaseNumberOfClosedBrackets(){
        _numberOfCloseBracket++;
    }

    /*
    Reset number of open and closed bracket.
     */
    public void resetNumberBrackets(){
        _numberOfOpenBracket = 1;
        _numberOfCloseBracket = 0;
    }

    /**
     * Check if a variable is exists in this scope1, or father scope1.
     * @param variable variable name to check.
     * @return true if exists, false otherwise.
     */
    public boolean isVariableExists(String variable){
        return _variables.containsKey(variable);
    }

    /**
     * Add new SavedParameter to variables. Checks name is not exists in both direct variables and methods.
     * @param savedParameter the parameter to add.
     */
    public void addVariable(SavedParameter savedParameter) throws Exception {
        _variables.put(savedParameter.getName(), savedParameter);
    }

    /**
     * Returns a variable according to given name. If not found returns null.
     * @param var param name
     * @return the found param, or null if not found.
     */
    public SavedParameter getVariable(String var){
        SavedParameter variable = null;
        try {
            variable =  _variables.get(var);
        } catch (NullPointerException e){}
        if (variable == null)
            try {
                variable = _parentScope.getVariable(var);
                if (_externalVariables.containsKey(variable.getName()))
                    variable = _externalVariables.get(variable.getName());
            }catch (NullPointerException e){
                return null;
            }
        return variable;
    }

    /**
     * Update a variable value (assuming variable exists).
     * @param parameter parameter to update
     * @throws Exception
     */
    public void updateVariable(SavedParameter parameter) throws Exception {
        SavedParameter s = getLocalVariable(parameter.getName());
        if (s != null) {
            if (s.isAFinalType())
                throw new Exception();
            s.setValue(parameter.getValue());
        } else {
            SavedParameter parentParam = _parentScope.getVariable(parameter.getName());
            if (!(parentParam != null && !parentParam.isAFinalType()))
                throw new Exception();
            parentParam = new SavedParameter(parentParam);
            parentParam.setValue(parameter.getValue());
            _externalVariables.put(parentParam.getName(), parentParam);
        }
    }

    public SavedParameter getLocalVariable(String variableName) {
        return _variables.get(variableName);
    }

    public void setParentScope(Scope parentScope) {
        _parentScope = parentScope;
    }
}
