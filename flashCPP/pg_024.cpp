#include <iostream>
#include "Sales_item.h"

/*
 * __author__ = @imflash217
 * __copyright__ = @flashAI, 2019
 *
 * Description: 
 */

int main(){
    Sales_item total;   // variable to hold data for next transaction

    // read the first transaction and ensure that there are data to process
    if (std::cin >> total){
        Sales_item trans;       // variable to hold the running sum

        // read and process the remaining transaction
        while (std::cin >> trans){
            if (total.isbn() == trans.isbn()){
                total += trans;
            } else{
                // print result for the total and update total, trans
                std::cout << total << std::endl;
                total = trans;
            }
        }
    } else{
        std::cerr << "No data provided" << std::endl;
        return -1;
    }    
    return 0;
}
