/**
 * @file
 *
 * @author    Javier S.
 * 20.03.2021 Corona_Time
 *
 * @brief   .a class to parse Gcode for CNC-Engraver
 *
 */

#include "gcode_parser.h"


GcodeParser::GcodeParser(std::string const & path, std::string const & OutPath)
{
   folder_path = path;

   //output_file = std::ofstream("./OutputFile.ngc");
   std::string Opath = OutPath + ("OutputFile.ngc");
   output_file = std::ofstream(Opath);
}


std::istream& operator>>(std::istream& str, GcodeParser& data)
{
    data.readNextRow(str);
    return str;
}


bool Is_Lim_Inputttt(std::string var_name){
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

bool Is_Lim_Outputttt(std::string var_name){
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
