package fileparsing;

/**
 * Simple section in flt file.
 */
public class SimpleSection {
    private String _filtering;
    private String _ordering;
    private int _lineNumber;

    SimpleSection(){
    }

    public void setFilter(String filter){
        _filtering = filter;
    }

    public void setOrder(String order){
        _ordering = order;
    }

    public void setNumberLine(int numberLine){
        _lineNumber = numberLine;
    }

    public String getFilter(){
        return _filtering;
    }

    public String getOrder(){
        return _ordering;
    }

    public int getNumberLine(){
        return _lineNumber;
    }
}
