%module Streams
%{
#define SWIG_FILE_WITH_INIT
#include "Streams.h"
%}
%ignore output_stream;
%ignore error_stream;

%include "Streams.h"
