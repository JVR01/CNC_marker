/*
 * csv_row.h
 *
 *  Created on: Mar 11, 2021
 *      Author: qscale
 */

#ifndef GcodeParser_H_
#define GcodeParser_H_

#include <iterator>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

//--#include "appbaselib/export/base_types.h"

//#include<string_view>

class GcodeParser
{
    public:
    
        GcodeParser(std::string const &path, std::string const & OutPath);
        
        std::string getCharPath()//std::string_view operator[](std::size_t index) const
        {
            return folder_path;
        }

        std::string operator[](std::size_t index) const //std::string_view operator[](std::size_t index) const
        {
            return std::string(&m_line[m_data[index] + 1], m_data[index + 1] -  (m_data[index] + 1)); //return std::string_view(
        }
        std::size_t size() const
        {
            return m_data.size() - 1;
        }
        void readNextRow(std::istream& str)
        {
            std::getline(str, m_line);

            m_data.clear();
            m_data.push_back(-1);
            std::string::size_type pos = 0;

            //uint32_t pos_end = 0; //m_line.find(" ");


            while((pos = m_line.find(';', pos)) != std::string::npos)
            {
                m_data.push_back(pos);
                ++pos;
                //pos_end = pos;
            }
            // This checks for a trailing comma with no data after it.
            //uint32_t pos_end = m_line.find("/r");
            //std::string text = m_line.substr(0, pos_end);
            //m_line+= ';';//test erase line
            pos   = m_line.size();
            m_data.push_back(pos);//m_data.push_back(pos);
        }

        int add_character(std::string const & character_str)
        {
          int result = 0;
          bool special_char = false;
          std::string::size_type posi = 0;
          std::string special_chars = "<> .-+-*#";

          if (  (posi = special_chars.find(character_str.c_str(), posi)  ) != std::string::npos) //(posi = character_str.find(';', posi)  ) != std::string::npos
          {
              special_char = true;
              std::cout << "++++++++Special character ++++++++++" << std::endl;
          }
#if  ROS_MELODIC
ROS_INFO("%s", "hallooooooooooooo");
#endif
            
          try {
                std::string char_path = folder_path + character_str + ".ngc";
                std::ifstream text_file(char_path.c_str());
                int number_of_lines = 0;
                if (text_file.is_open()) {
                        std::string line;
                    
                        while (std::getline(text_file, line)) {
                            number_of_lines++;

                            if (output_file.is_open()) 
                            {
                              output_file << line << std::endl;
                              std::cout << line << std::endl;
                            }
                            else{result = 1001;}
                            
                        }
                        //--output_file << "" << std::endl;
                        text_file.close();
                        //-->std::cout <<"Number of lines Found: "<< number_of_lines << std::endl;
                }
                else
                {
                    throw (character_str);
                }
            } catch (const std::overflow_error& e) {
                // this executes if f() throws std::overflow_error (same type rule)
                std::cout <<"overflow_error " << std::endl;
            } catch (const std::runtime_error& e) {
                // this executes if f() throws std::underflow_error (base class rule)
                std::cout <<"underflow_error " << std::endl;
            } catch (const std::exception& e) {
                // this executes if f() throws std::logic_error (base class rule)
                std::cout <<"logic_error " << std::endl;
            } 
            catch (std::string const & word) {
               result = 1;    
               std::cout << "Error -> Character not found on the list" << std::endl;;
               std::cout << "The faulty character is: " << word << std::endl;
            }

          return result;

        }
        int add_phrase(std::string const & phrase)
        {
            //int add_character(std::string const & character_str)
            int result = 0;
            std::string str = phrase;//("Test string");

            /*for ( std::string::iterator it=str.begin(); it!=str.end(); ++it)
            {
               std::cout << *it <<"--";
              
            }
            
            std::cout << '\n';*/

            for (std::string::size_type i = 0; i < str.size(); i++) {
                std::cout << str[i] << ' ';  
                std::string s(1, str[i]);
                result += add_character(s); // if faulty returns a 0
                if(i <  str.size()-1 ){add_transition_code();}
            }
            add_end_code();
            std::cout <<"faulty Characters -> "<< result <<" / "<< str.size() << std::endl;

            return result;
        }


        void add_transition_code()
        {
          output_file << "G00 X10.0000Y0.0000" << std::endl;
          output_file << "G54" << std::endl;
          output_file << "G10 L20 P2 X0 Y0" << std::endl;
          output_file << "G55" << std::endl;
          //--output_file << "" << std::endl;
          //output_file << "G00 X20.0000Y0.0000" << std::endl;
          //output_file << "G56" << std::endl;
          //output_file << "G10 L20 P3 X0 Y0" << std::endl;
        }
        void add_end_code()
        {
          output_file << "G54 (First ofset)" << std::endl;
          output_file << "M3  (Stop Spindle -- Go up servo)" << std::endl;
          output_file << "G00 X0.0000 Y0.0000" << std::endl;
          output_file << "M2" << std::endl;
          output_file << "%" << std::endl;
          output_file.close();
        }
        void add_start_code()
        {
          output_file << "$X" << std::endl;
          output_file << "$G" << std::endl;
          output_file << "$X" << std::endl;
           
          //output_file << "%" << std::endl;
          output_file << "M3" << std::endl;
          output_file << "G21 (All units in mm)" << std::endl;
          output_file << "G54 (First ofset)" << std::endl;
          output_file << "G1 F500" << std::endl;
          output_file << "M5 S120" << std::endl;
          output_file << "M3" << std::endl;
          output_file << "$H" << std::endl; 
          //--output_file << "" << std::endl;
        }
        
    private:
        std::string         m_line;
        std::vector<int>    m_data;
        std::string         folder_path; //path of the .ngc files
        
        std::ofstream output_file;
};

std::istream& operator>>(std::istream& str, GcodeParser& data);
bool Is_Lim_Inputttt(std::string var_name);
/*

int main()
{
    std::ifstream       file("plop.csv");

    GcodeParser              row;
    while(file >> row)
    {
        std::cout << "4th Element(" << row[3] << ")\n";
    }
}*/



#endif /* LIMITER3_SRC_CSV_ROW_H_ */
