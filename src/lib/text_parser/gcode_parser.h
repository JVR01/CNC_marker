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

enum class ErrorCode
{
    SUCCESS = 0,
    OUTPUT_FILE_NOT_OPEN = 1001,
    INPUT_FILE_NOT_OPEN = 1002,
    UNKNOWN_ERROR = 1003
};

class GcodeParser
{
public:
    GcodeParser(std::string const &path, std::string const &OutPath);

    int8_t MAX_ROW_LENGTH_BIG = 6U;

    std::string getCharPath() // std::string_view operator[](std::size_t index) const
    {
        return folder_path;
    }

    std::string operator[](std::size_t index) const // std::string_view operator[](std::size_t index) const
    {
        return std::string(&m_line[m_data[index] + 1], m_data[index + 1] - (m_data[index] + 1)); // return std::string_view(
    }

    std::size_t size() const
    {
        return m_data.size() - 1;
    }

    void readNextRow(std::istream &str)
    {
        std::getline(str, m_line);

        m_data.clear();
        m_data.push_back(-1);
        std::string::size_type pos = 0;

        // uint32_t pos_end = 0; //m_line.find(" ");

        while ((pos = m_line.find(';', pos)) != std::string::npos)
        {
            m_data.push_back(pos);
            ++pos;
            // pos_end = pos;
        }
        // This checks for a trailing comma with no data after it.
        // uint32_t pos_end = m_line.find("/r");
        // std::string text = m_line.substr(0, pos_end);
        // m_line+= ';';//test erase line
        pos = m_line.size();
        m_data.push_back(pos); // m_data.push_back(pos);
    }

    int add_character(std::string const &character_str)
    {
        int result = 0;
        bool special_char = false;
        std::string::size_type posi = 0;
        std::string special_chars = "<> .-+-*#";

        if ((posi = special_chars.find(character_str.c_str(), posi)) != std::string::npos)
        {
            special_char = true;
            std::cout << "++++++++Special character ++++++++++" << std::endl;
        }

#if ROS_MELODIC
        ROS_INFO("%s", "Hello fro ROS melodic");
#endif

        try
        {
            std::string char_path = folder_path + character_str + ".ngc";
            std::ifstream text_file(char_path.c_str());
            int number_of_lines = 0;
            if (text_file.is_open())
            {
                std::string line;
                std::cout << "++++++++File opened for char: " << character_str << std::endl;

                while (std::getline(text_file, line))
                {
                    number_of_lines++;

                    if (output_file.is_open())
                    {
                        output_file << line << std::endl;
                        std::cout << line << std::endl;
                    }
                    else
                    {
                        result = 1001;
                    }
                }
                //--output_file << "" << std::endl;
                text_file.close();
                //-->std::cout <<"Number of lines Found: "<< number_of_lines << std::endl;
            }
            else
            {
                std::cout << "xxxxxx--File NOT opened for char: " << character_str << std::endl;
                std::cout << "char path was this: " << char_path << std::endl;
                throw(character_str); // without this it wont through the number of wrong chars
            }
        }
        catch (const std::overflow_error &e)
        {
            // this executes if f() throws std::overflow_error (same type rule)
            std::cout << "overflow_error " << std::endl;
        }
        catch (const std::runtime_error &e)
        {
            // this executes if f() throws std::underflow_error (base class rule)
            std::cout << "underflow_error " << std::endl;
        }
        catch (const std::exception &e)
        {
            // this executes if f() throws std::logic_error (base class rule)
            std::cout << "logic_error " << std::endl;
        }
        catch (std::string const &word)
        {
            result = 1;
            std::cout << "Error -> UNIMPLEMENTED EXEPTION" << std::endl;
            std::cout << "Error -> Character not found on the list" << std::endl;
            std::cout << "The faulty character is: " << word << std::endl;
        }

        return result;
    }

    int add_character_2(std::string const &character_str)
    {
        int result = 0;

        bool special_char = false;
        std::string::size_type posi = 0;
        std::string special_chars = "<>.-+-*#";

        if ((posi = special_chars.find(character_str.c_str(), posi)) != std::string::npos)
        {
            special_char = true;
            std::cout << "++++++++Special character ++++++++++" << std::endl;
            return 1; // character wont be found, just return ToDo
        }

#if ROS_MELODIC
        ROS_INFO("%s", "Hello fro ROS melodic");
#endif

        try
        {
            std::string current_cahr_code = getCharacterGcode(character_str, folder_path + "characters_Gcode.txt");

            if (character_str == " ")
            {
                current_cahr_code = getCharacterGcode("space", folder_path + "characters_Gcode.txt");
            }

            int number_of_lines = 0;

            if (current_cahr_code != "")
            {
                std::cout << "++++++++Trying to add char: " << character_str << std::endl;

                std::istringstream f(current_cahr_code);
                std::string line;
                while (std::getline(f, line))
                {
                    // std::cout <<"found line: "<< line << std::endl;

                    number_of_lines++;

                    if (output_file.is_open())
                    {
                        output_file << line << std::endl;
                        // std::cout << "Adding line to Output: "<<line << std::endl;
                    }
                    else
                    {
                        std::cout << "xxxxxx--Output file was not open: " << character_str << std::endl;
                        result = 1001;
                    }
                }

                //-->std::cout <<"Number of lines Found: "<< number_of_lines << std::endl;
            }
            else
            {
                std::cout << "xxxxxx--Could not find char: " << character_str << std::endl;
                std::cout << "chars Gcode path was this: " << folder_path + "characters_Gcode.txt" << std::endl;
                throw(character_str); // without this it wont through the number of wrong chars
            }
        }
        catch (const std::overflow_error &e)
        {
            // this executes if f() throws std::overflow_error (same type rule)
            std::cout << "overflow_error " << std::endl;
        }
        catch (const std::runtime_error &e)
        {
            // this executes if f() throws std::underflow_error (base class rule)
            std::cout << "underflow_error " << std::endl;
        }
        catch (const std::exception &e)
        {
            // this executes if f() throws std::logic_error (base class rule)
            std::cout << "logic_error " << std::endl;
        }
        catch (std::string const &word)
        {
            result = 1;
            std::cout << "Error -> UNIMPLEMENTED EXEPTION" << std::endl;
            std::cout << "The faulty character is: " << word << std::endl;
        }

        return result;
    }

    int add_phrase(std::string const &phrase)
    {
        // int add_character(std::string const & character_str)
        int result = 0;
        std::string str = phrase; //("Test string");

        uint8_t raws_number = str.size() / MAX_ROW_LENGTH_BIG;         // 12/7 = 1
        uint8_t residual_raw_number = str.size() % MAX_ROW_LENGTH_BIG; // 12/7--> 5
        raws_number = (residual_raw_number > 0) ? raws_number++ : raws_number;

        std::cout << "Doing so many raws: " << raws_number << std::endl;

        for (uint8_t r = 0U; r < raws_number; r++)
        {
            add_transition_code_vertical_up(); // start n rows up, so that it keeps writing down
        }

        uint8_t drawn_chars_count = 0U;
        bool down_trans_recent = false;

        for (std::string::size_type i = 0; i < str.size(); i++)
        {
            std::cout << str[i] << ' ';
            std::string s(1, str[i]);

            // 6>5
            // 5>5

            /*if(drawn_chars_count > MAX_ROW_LENGTH_BIG-1)// i will get to i=10 then shoud do this from i=6 on
            {
                add_transition_code_vertical_down();
                drawn_chars_count = 0U;
                down_trans_recent = true;
            }*/

            // result += add_character(s); // if faulty returns a 0
            result += add_character_2(s); // if faulty returns a 0

            //&& (!down_trans_recent)
            //&& (drawn_chars_count == MAX_ROW_LENGTH_BIG-1)
            //(drawn_chars_count + 1 != MAX_ROW_LENGTH_BIG-1)
            if ((i < str.size() - 1)) // Dont do if vert_down added
            {
                if (drawn_chars_count >= MAX_ROW_LENGTH_BIG - 1) // i will get to i=10 then shoud do this from i=6 on
                {
                    add_transition_code_vertical_down();
                    drawn_chars_count = 0U;
                    down_trans_recent = true;
                }
                else
                {
                    add_transition_code();
                    // down_trans_recent = false;//reset flag
                }
            }

            drawn_chars_count++;
        }

        add_end_code();

        std::cout << "faulty Characters -> " << result << " / " << str.size() << std::endl;

        return result;
    }

    int add_special_symbol(const std::string &symbol_str)
    {
        int result = static_cast<int>(ErrorCode::SUCCESS);

        try
        {
            // Construct the full path to the input file
            std::string current_symbol_code = folder_path + symbol_str + ".gcode";
            std::ifstream text_file(current_symbol_code);

            if (!text_file.is_open())
            {
                std::cerr << "Error: Could not open file for symbol: " << symbol_str << std::endl;
                return static_cast<int>(ErrorCode::INPUT_FILE_NOT_OPEN);
            }

            if (!output_file.is_open())
            {
                std::cerr << "Error: Output file is not open." << std::endl;
                return static_cast<int>(ErrorCode::OUTPUT_FILE_NOT_OPEN);
            }

            std::string line;
            std::cout << "Processing file for symbol: " << symbol_str << std::endl;

            // Read the input file line by line and write to the output file
            while (std::getline(text_file, line))
            {
                output_file << line << std::endl;
                std::cout << line << std::endl;
            }

            text_file.close();
        }
        catch (const std::exception &e)
        {
            std::cerr << "Exception occurred: " << e.what() << std::endl;
            result = static_cast<int>(ErrorCode::UNKNOWN_ERROR);
        }

        return result;
    }

    void add_transition_code()
    {
        output_file << "(TRANS_RIGHT)" << std::endl;
        output_file << "G00 X8.000 Y0.0000" << std::endl;
        output_file << "G54" << std::endl;
        output_file << "G10 L20 P2 X0 Y0" << std::endl;
        output_file << "G55" << std::endl;
    }

    void add_transition_code_vertical_up()
    {
        output_file << "G00 X0.000 Y8.000" << std::endl;
        output_file << "G54" << std::endl;
        output_file << "G10 L20 P2 X0 Y0" << std::endl;
        output_file << "G55" << std::endl;
    }

    void add_transition_code_vertical_down()
    {
        output_file << "(TRANS_DOWN)" << std::endl;         // 8*6 = 48
        output_file << "G00 X-40.000 Y-8.000" << std::endl; // 8*6 = 48
        output_file << "G54" << std::endl;
        output_file << "G10 L20 P2 X0 Y0" << std::endl;
        output_file << "G55" << std::endl;
    }

    void add_end_code()
    {
        output_file << "G54 (First ofset)" << std::endl;
        output_file << "M3 S90" << std::endl; // servo up
        output_file << "G4 P1.000" << std::endl;
        output_file << "G00 X0.0000 Y0.0000" << std::endl;
        output_file << "M2" << std::endl;
        output_file << "%" << std::endl;
        output_file.close();
    }

    void add_start_code()
    {
        output_file << "$X" << std::endl;
        output_file << "$X" << std::endl;
        output_file << "G90" << std::endl;
        output_file << "G21 (All units in mm)" << std::endl;
        output_file << "G54 (First ofset)" << std::endl;
        output_file << "M3 S90" << std::endl; // servo up
        output_file << "G4 P1.000" << std::endl;
        output_file << "$H" << std::endl;
        output_file << "G4 P1.000" << std::endl;
        output_file << "M3 S90" << std::endl; // servo up
        output_file << "G4 P1.000" << std::endl;
        output_file << "G1 F500.000" << std::endl;
        //--output_file << "" << std::endl;
    }

    std::string getCharacterGcode(const std::string &character, const std::string &filePath)
    {
        std::ifstream file(filePath); // Open the file
        if (!file.is_open())
        {
            std::cerr << "Error: Could not open file at path " << filePath << std::endl;
            return "";
        }

        std::string line;
        std::string targetHeader = "———character: " + character + " ———-";
        std::string gcode = "";
        bool foundCharacter = false;

        while (std::getline(file, line))
        {
            // Check if the current line is the header for the target character
            if (line.find(targetHeader) != std::string::npos)
            {
                foundCharacter = true;
                continue; // Skip the header line
            }

            // If we've found the character, collect its G-code
            if (foundCharacter)
            {
                // Stop if we encounter the next character's header or end of file
                if (line.find("———character:") != std::string::npos)
                {
                    break;
                }
                gcode += line + "\n"; // Append the line to the G-code string
            }
        }

        file.close(); // Close the file

        if (!foundCharacter)
        {
            std::cerr << "Error: Character '" << character << "' not found in the file." << std::endl;
            return "";
        }

        return gcode;
    }

private:
    std::string m_line;
    std::vector<int> m_data;
    std::string folder_path; // path of the .ngc files

    std::ofstream output_file;
};

std::istream &operator>>(std::istream &str, GcodeParser &data);
bool Is_Lim_Inputttt(std::string var_name);

#endif /* LIMITER3_SRC_CSV_ROW_H_ */
