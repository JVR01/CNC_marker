#include <iostream>
#include "gcode_parser.h"

using namespace std;

int main()
{
    std::string path_ngc = "../../../Characters/" ; //define Characters source
    //std::ofstream output_file("./OutputFile.txt"); //writes out the results
    GcodeParser GCode(path_ngc);
    //CSVRow row;
    std::string str_character = "A";
    //std::system("ls ../../../Characters/*.ngc | xargs -n 1 basename >./newtestcase/EXCEL/TC001/names.txt");
    //exceuting this only file name will be copied into the .txt, without path

    std::string char_path = path_ngc + str_character + ".ngc";
    std::fstream char_file(char_path.c_str());
    std::ifstream CsvFile(char_path.c_str());

    bool nix = Is_Lim_Inputttt(char_path);
     /*ofstream: Stream class to write on files
    ifstream: Stream class to read from files//ifstream represents the file
    fstream: Stream class to both read and write from/to files.*/
    GCode.add_start_code();
    
    int U = GCode.add_character("A");
    U = GCode.add_character(" ");
    U = GCode.add_character(";");
    U = GCode.add_character("B");
    U = GCode.add_character("C");

    U = GCode.add_phrase("moquiAto");
    /*GCode.add_transition_code();
    U = GCode.add_character("B");
    GCode.add_transition_code();
    U = GCode.add_character("C");
    GCode.add_end_code();*/

    //----output_file << "RatedCapacity: " << char_path << std::endl;
    //--output_file << char_file << std::endl;
    //std::cout << std::ifstream(char_path.c_str()).rdbuf();
    cout << char_path << endl;
    cout << "hey Dude!" << endl;
    return 0;
}

    /*int i = 0;
    while(CsvFile >> GCode)
    {
        //--std::cout << "Column " << i << ": " << GCode[0] << std::endl; //returns the content of every Raw[0] in CsvFile (Column 0)
        //output_file << char_file << std::endl;
        i++;
    }
    CsvFile.clear();
    CsvFile.seekg(0, std::ios::beg);

    int number_of_lines = 0;
    if (CsvFile.is_open()) {
        std::string line;
        while (std::getline(CsvFile, line)) {
            number_of_lines++;
            output_file << line << std::endl;
            std::cout << line << std::endl;
        }
        CsvFile.close();
        std::cout <<"Number of lines Found: "<< number_of_lines << std::endl;
    }*/