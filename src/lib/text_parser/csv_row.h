/*
 * csv_row.h
 *
 *  Created on: Mar 11, 2021
 *      Author: qscale
 */

#ifndef CSV_ROW_H_
#define CSV_ROW_H_

#include <iterator>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

//--#include "appbaselib/export/base_types.h"

//#include<string_view>

class CSVRow
{
    public:
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
    private:
        std::string         m_line;
        std::vector<int>    m_data;
};



/*

int main()
{
    std::ifstream       file("plop.csv");

    CSVRow              row;
    while(file >> row)
    {
        std::cout << "4th Element(" << row[3] << ")\n";
    }
}*/
class Data_Element
{
    public:
        // Setter
        /*void name(std::string n) {
          name_ = n;
        }
        // Getter
        std::string name() {
          return name_;
        }*/

        std::string name;
        std::string value;
        std::string var_IO;
        std::string type;

        void show_me() {
            std::cout << "---------------"<< std::endl;
            std::cout << "Name: " << name  << std::endl;
            std::cout << "Value: " << value << std::endl;
            std::cout << "Var_IO: " << var_IO << std::endl;
            std::cout << "Type: " << type  << std::endl;
        }
    private:
        //std::string name_;
};


#endif /* LIMITER3_SRC_CSV_ROW_H_ */
