%module main

%{
#include "OptionHandler.h"
%}

%include <std_string.i>

%include "OptionHandler.h"

%{
#define SWIG_FILE_WITH_INIT
#include "Streams.h"
%}
%ignore output_stream;
%ignore error_stream;

%include "Streams.h"

%{
#include "Options.h"
%}

%include "Options.h"
