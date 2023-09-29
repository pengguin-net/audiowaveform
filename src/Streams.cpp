//
// Created by user on 9/29/23.
//

#include "Streams.h"
#include <sstream>

// Define the output and error std::ostringstream objects
std::ostringstream output;
std::ostringstream error;

// Define the output and error std::ostream references
std::ostream& output_stream = output;
std::ostream& error_stream = error;
