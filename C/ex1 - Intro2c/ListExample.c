#include "MyLinkedList.h"
#include <stdio.h>
#include <assert.h>

int main() 
{
    char* array[]={"2","4","6","2","12","77","99"}; 
	 int i;    
    
    MyLinkedListP l1 = createList(),l2,l3;
    printList(l1);		    
    for(i=0; i<7; i++)    
    {
    	insertFirst(l1,array[i]);
    }
    printList(l1);
    
    l2 = cloneList(l1);
    l3 = cloneList(l2);
    
	 printf("'77' appears %d timed in list\n",isInList(l1,"77"));
	 printf("l1 size=%d\n",getSize(l1));
	 printf("remove '4' from l1 -> removed %d times\n",removeData(l1,"4"));    
	 printf("remove '2' from l1 -> removed %d times\n",removeData(l1,"2"));
	 
    printList(l1);
    printList(l2);
    freeList(l1);
    freeList(l2);

	 printf("\nmake a mess to check everything is ok\n");
	 int j,res;
	 for (j=0;j<7;j++) 
	 {    
		for(i=0; i<7; i++) 
		{
        insertFirst(l3,array[i]);
      }
     printList(l3);     

     for(i=0; i<7; i++) 
     {
        res= removeData(l3,array[i]);
        if (res>0) 
        {
        assert(res>=0);
        }
     }
     printList(l3);
    }        
    freeList(l3);

    return 0;
}