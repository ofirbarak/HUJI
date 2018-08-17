package oop.ex6.main;

import oop.ex6.general.GeneralHelpFunctions;
import oop.ex6.handleLine.HandleSJavaType;
import oop.ex6.handleLine.HandleSavedParam;
import oop.ex6.handleLine.ScopeHandler;
import oop.ex6.handleLine.functions.SJavaFunctionsValidation;
import oop.ex6.scope.FunctionScope;
import oop.ex6.scope.MainScope;
import oop.ex6.scope.Scope;

import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.LineNumberReader;

/**
 * The REAL parser for checking a document;
 */
public class Parser {
    private static Scope _currentScope;

    private static FileInputStream _fileInputStream;
    private static LineNumberReader _reader;

    /*
    Reset the parser class
     */
    public static void resetParser(){
        MainScope.reset();
        ScopeHandler.resetScopeHandler();
    }

    /*
    Runs the checks.
    Algorithm: Firstly, creates the main scope, pass all file and checks globals and methods declarations and
    adds them to mainScope's maps.
    After that set the cursor to the beginning of the file and pass line after line and checks:
        ** Comments and spaces lines are automatically checked and skipped
        - If current scope is the main scope so:
            - If it's variable declaration we already passed it
            - If it's a method declaration we already passed it, and we just need to update the current scope
            - If it's 'if' or 'while' type that's an error
        - Otherwise current scope is not the main scope and we act like this:
            - If it's a variable declaration do the checks
            - If it's 'if' or 'while' do the checks - update to the new scope and...
            - otherwise that's an exception
     */
    public static void run(FileInputStream fileInputStream, String arg) throws Exception {
        _reader = new LineNumberReader(new InputStreamReader(new FileInputStream(arg)));
        _fileInputStream = fileInputStream;
        Scope mainScope = MainScope.getInstance();
        updateScope(mainScope);
        passAndUpdateMainScope();

        String currentLine, lastLine = null;
        while ( (currentLine = _reader.readLine()) != null) { // Parse all file
            runsALine(currentLine, lastLine);
            if (lastLine!= null && _currentScope.isScopeEnded()){
                if (_currentScope instanceof FunctionScope && !lastLine.matches(HandleSJavaType.RETURN_REGEX))
                        throw new Exception();
                updateScope(_currentScope.getParentScope());
            }
            lastLine = currentLine;
        }
    }

    // ----------------------- First pass methods ----------------------------------------
    private static void passAndUpdateMainScope() throws Exception {
        /*
        Pass all file and adds methods and variables. Set the cursor to the beginning of the file.
        Also, Pass all file and check if variable declared without init value the following line is
        assign value. (If variable not assign value in the followed line if we try to use this
        variable we get an error).
         */
        String line;
        while ((line = _reader.readLine()) != null) {
            String[] split = GeneralHelpFunctions.getsFirstWordAndTheRestOfTheString(line);
            if (split[0] != null) {
                if (HandleSJavaType.isTypeIsVariable(split[0]))// If it's declaration of variable or method
                    HandleSJavaType.checkVariableDeclaration(split[0], split[1]);
                else if (split[0].matches(HandleSJavaType.VOID)) {
                    Scope scope = HandleSJavaType.checkMethodDeclaration(split[0], split[1]);

                    skipSectionContent(scope);
                    scope.resetNumberBrackets();
                }
            }
        }
        // Update cursor
        _reader = new LineNumberReader(new InputStreamReader(_fileInputStream));
    }

    private static void updateScope(Scope newScope) {
        // Update current scope and the scope in ScopeHandler class
        _currentScope = newScope;
        ScopeHandler.updateScope(newScope);
    }

    private static void skipSectionContent(Scope scope) throws Exception {
        String line;
        while (!scope.isScopeEnded() && (line = _reader.readLine()) != null){
            if (line.matches(HandleSJavaType.CLOSE_BLOCK_REGEX))
                scope.increaseNumberOfClosedBrackets();
        }
        scope.resetNumberBrackets();
    }

    // -------------------------------- End first pass methods ---------------------------------------

    /*
    Checks for comments and empty line or close bracket
     */
    private static boolean generalChecks(String line) throws Exception {
        if (line == null) // todo: check if we need this if
            return true;
        if (GeneralHelpFunctions.isOnlySpacesInTheString(line))
            return true;
        if (line.matches(HandleSJavaType.CLOSE_BLOCK_REGEX)) {
            _currentScope.increaseNumberOfClosedBrackets();
            return true;
        }
        if (line.matches(HandleSJavaType.COMMENT_REGEX))
            return true;
        if (line.matches(HandleSJavaType.RETURN_REGEX)) {
            if (MainScope.isMainScope(_currentScope))
                throw new Exception();
            return true;
        }
        return false;
    }

    /*
    Check each line if it's from a known s-java type, if yes class HandleSJavaType, if not checks if value
    declared.
    */
    private static void runsALine(String line, String lastLine) throws Exception {
        if (generalChecks(line))
            return;
        String[] split = GeneralHelpFunctions.getsFirstWordAndTheRestOfTheString(line);
        if (split[0] != null && HandleSJavaType.isAKnownSJavaWord(split[0])) {
            if (HandleSJavaType.isTypeIsVariable(split[0])) {
                if (!MainScope.isMainScope(_currentScope))
                    HandleSJavaType.checkVariableDeclaration(split[0], split[1]);
            } else if (split[0].equals(HandleSJavaType.VOID)) {
                if (MainScope.isMainScope(_currentScope))
                    updateScope(((MainScope) _currentScope).getFunctionScope(
                            SJavaFunctionsValidation.getName(split[1])));
                else // We already can throw an exception because we passed all the function suppose to be in main scope.
                    throw new Exception();
            }
        }
        else {
            split = GeneralHelpFunctions.getUntilFirstOpenBracketAndRest(line);
            if (split[0] != null && HandleSJavaType.isTypeIsSupposeToGenerateNewScope(split[0])) {
                if (MainScope.isMainScope(_currentScope))
                    throw new Exception();
                updateScope(HandleSJavaType.checkIfWhileAndGetsNewScope(split[1]));
            } else {
                getLastLineVariableName(lastLine);
                if (!HandleSavedParam.checkAssigningValueToVariable(line) &&
                        !(HandleSavedParam.checkAMethodCall(line)))
                    throw new Exception();
            }
        }
    }

    private static void getLastLineVariableName(String line) {
        String ret = null;
        try {
            String[] split = GeneralHelpFunctions.getsFirstWordAndTheRestOfTheString(
                    GeneralHelpFunctions.getStringWithoutSemicolon(line));
            if (split[0] != null)
                if (HandleSJavaType.isTypeIsVariable(split[0]))
                    ret = split[1].split("=")[0];
        } catch (Exception e){}
        ScopeHandler._nameOfLastLine = ret;
    }
}
