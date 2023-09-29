import main
import sys
import tempfile
import os
import json

opt = main.OptionHandler()
options = main.Options()

options.setInputFilename("/mnt/devdrive/files/projects/pengguin/files/bf51da71b26de5cd2790edeeee7f2ed62b7f5e38d18764663bb8bc854d663618.wav")
options.setOutputFormat("json")
options.setInputFormat("wav")
options.handleZoomOption("256")
options.handleAmplitudeScaleOption("1.0")

# Use 'with' to handle the temp file lifecycle
with tempfile.NamedTemporaryFile(delete=True, suffix=".json") as temp_file:
    options.setOutputFilename(temp_file.name)
    assert opt.run(options) is True
    temp_file.seek(0)    
    file_contents = temp_file.read()
    out = json.loads(file_contents.decode('utf-8'))

print(out)
