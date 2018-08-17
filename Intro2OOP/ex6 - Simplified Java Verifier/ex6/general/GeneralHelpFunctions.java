package oop.ex6.general;

import oop.ex6.Exceptions.NameException;
import oop.ex6.Exceptions.NoCircleOpenBracket;
import oop.ex6.Exceptions.NoSemicolonAtEndsOfTheLine;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * General functions for parsing.
 */
public class GeneralHelpFunctions {
    static final String EMPTY_LINE = "^\\s*$";
    private static final String EMPTY_CELL = "";
    private static final String FIRST_WORD_AND_REST_OF_STRING_REGEX = "^\\s*(\\w+)\\s+(.*)";
    private static final String WORD_TO_OPEN_BRACKET_REGEX = "^\\s*(\\w+)\\s*(\\(.*)";
    private static final String STRING_WITHOUT_SEMICOLON_REGEX = "^(.*)\\s*;\\s*$";
    private static final String WORD_TO_CIRCLE_OPEN_BRACKET_REGEX = "^(.*)\\s*[{]\\s*$";

    /*
    Gets the First sequence of char(s) and the rest of the string. If String contains only
    spaces returns {"",""}.
     */
    public static String[] getsFirstWordAndTheRestOfTheString(String line){
        String[] ret = new String[2];
        if (isOnlySpacesInTheString(line)) {
            ret[0] = EMPTY_CELL;
            ret[1] = EMPTY_CELL;
            return ret;
        }
        Pattern pattern = Pattern.compile(FIRST_WORD_AND_REST_OF_STRING_REGEX);
        Matcher matcher = pattern.matcher(line);
        if (matcher.find()){
            ret[0] = matcher.group(1).trim();
            ret[1] = matcher.group(2);
        }
        else {
            ret[0] = null;
            ret[1] = null;
        }
        return ret;
    }

    public static String[] getUntilFirstOpenBracketAndRest(String line){
        String[] ret = new String[2];
        Pattern pattern = Pattern.compile(WORD_TO_OPEN_BRACKET_REGEX);
        Matcher matcher = pattern.matcher(line);
        if (matcher.find()){
            ret[0] = matcher.group(1).trim();
            ret[1] = matcher.group(2);
        }
        else {
            ret[0] = null;
            ret[1] = null;
        }
        return ret;
    }

    public static boolean isOnlySpacesInTheString(String line){
        return line.matches(EMPTY_LINE);
    }

    /*
    If semicolon exists returns the string without it, otherwise return null.
     */
    public static String getStringWithoutSemicolon(String line){
        Pattern pattern = Pattern.compile(STRING_WITHOUT_SEMICOLON_REGEX);
        Matcher matcher = pattern.matcher(line);
        if (!matcher.find())
            return null;
        return matcher.group(1);
    }

    /*
    Checks the variable name.
     */
    public static String getsAndChecksName(String name) throws Exception {
        Pattern p = Pattern.compile("^\\s*[\\w\\d]+\\s*$");
        Matcher m = p.matcher(name);
        if (!m.matches())
            throw new NameException();
        p = Pattern.compile("^\\s*([\\d]+)\\s*$");
        m = p.matcher(name);
        if (m.matches()) // If the name is empty and without whitespaces.
            throw new NameException();
        p = Pattern.compile("^\\s*_+.*\\s*$");
        m = p.matcher(name); // get a matcher object
        if (m.matches()) // If name starts with more than one underscore
            p = Pattern.compile("^\\s*_\\s*$"); // starts with exactly one underscore.
        else
            p = Pattern.compile("^\\s*\\d+.*\\s*$"); // starts with a digit
        m = p.matcher(name);
        if (m.matches())
            throw new NameException();
        return name.trim();
    }

    /*
   If open bracket exists returns the string without it, throw an exception.
    */
    public static String checksAndGetsLineWithoutOpenBracket(String line) throws Exception {
        Pattern pattern = Pattern.compile(WORD_TO_CIRCLE_OPEN_BRACKET_REGEX);
        Matcher matcher = pattern.matcher(line);
        if (!matcher.find())
            throw new NoCircleOpenBracket();
        return matcher.group(1);
    }

    /*
    If line is empty return null, if line doesn't contains a semicolon throw an exception.
     */
    public static String checksAndGetsLineWithoutSemicolon(String line) throws Exception {
        if (GeneralHelpFunctions.isOnlySpacesInTheString(line))
            return null;
        String retLine = GeneralHelpFunctions.getStringWithoutSemicolon(line);
        if (retLine == null)
            throw new NoSemicolonAtEndsOfTheLine();
        return retLine;
    }

    public static String[] getSplitParams(String paramsAtOnePiece){
        if (paramsAtOnePiece.indexOf(',') != -1)
            if (paramsAtOnePiece.matches(".*,\\s*")) // If end with ','
                return null;
        return paramsAtOnePiece.split(",");
    }
}
