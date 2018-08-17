package oop.ex6.scope;

import oop.ex6.handleLine.HandleSJavaType;

/**
 * Class that represents a new declaration parameter(variable/method).
 */
public class SavedParameter{
    private String _name;
    private String _type;
    private String _value;
    private String _modifier = "default";

    /**
     * Generate a new equal parameter to save.
     * @param s saved parameter
     */
    public SavedParameter(SavedParameter s){
        this(s._name, s._type, s._value);
    }

    /**
     * Generate a new parameter to save.
     * @param name name of param
     * @param value param value
     * @param type param type
     */
    public SavedParameter(String name, String value, String type){
        _name = name;
        _type = type;
        _value = value;
    }

    /**
     * Returns param value.
     * @return param value.
     */
    public String getValue(){
        return _value;
    }

    /**
     * Returns param type
     * @return param type
     */
    public String getType(){
        return _type;
    }

    /**
     * Returns param name
     * @return param name
     */
    public String getName(){
        return _name;
    }

    /**
     *  Checks if two parameter are equal (in type)
     * @param other parameter to check
     * @return true if yes, false  otherwise
     */
    public boolean equals(SavedParameter other){
        String thisType = this.getType();
        String otherType = other.getType();
        if (thisType.equals(HandleSJavaType.BOOLEAN) && !otherType.equals(HandleSJavaType.BOOLEAN))
            return otherType.equals(HandleSJavaType.DOUBLE) || otherType.equals(HandleSJavaType.INT);
        else if (!thisType.equals(HandleSJavaType.BOOLEAN) && otherType.equals(HandleSJavaType.BOOLEAN))
            return thisType.equals(HandleSJavaType.DOUBLE) || thisType.equals(HandleSJavaType.INT);
        else
            return _type.equals(other._type);
    }

    /**
     * Change param modifier
     * @param newModifier new modifier
     */
    public void setModifier(String newModifier){
        _modifier = newModifier;
    }

    public boolean isAFinalType(){
        return _modifier.equals("final");
    }

    public void setValue(String value) {
        _value = value;
    }


}
