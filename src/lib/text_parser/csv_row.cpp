/**
 * @file
 *
 * @author    Javier S.
 * 
 *
 * @brief   .CSV row Class
 *
 */

#include "csv_row.h"



std::istream& operator>>(std::istream& str, CSVRow& data)
{
    data.readNextRow(str);
    return str;
}


bool Is_Lim_Input(std::string var_name){
    bool result = false;
    std::string word;

    //std::getline(var_name.c_str(), word, '.');
    word.find("LIMITER_INPUT");
    //string substr (size_t pos = 0, size_t len = npos) const;
    std::string delimiter = ".";
    word = var_name.substr(0, var_name.find(delimiter));

    if(word == "LIMITER_INPUT"){
        result = true;
    }
    //http://www.cplusplus.com/reference/string/string/find/
    return result;
}

bool Is_Lim_Output(std::string var_name){
    bool result = false;
    std::string word;

    //std::getline(var_name.c_str(), word, '.');
    word.find("LIMITER_OUTPUT");
    //string substr (size_t pos = 0, size_t len = npos) const;
    std::string delimiter = ".";
    word = var_name.substr(0, var_name.find(delimiter));

    if(word == "LIMITER_OUTPUT"){
        result = true;
    }
    //http://www.cplusplus.com/reference/string/string/find/
    return result;
}
