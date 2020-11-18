# Formatting Transcripts for DeepSpeech

1. Load in the original transcripts (*.xlsx files) into libreoffice or Excel, and copy-replace all newlines in the transcripts column with a space (this might occur with multiple speakers). Then export the data as a ".csv" file, using tilde "~" as the delimiter (because there's lots of formatting issues, but no wild tildes)
2. Run ./clean-transcripts.sh on the ".csv" file which was exported above 
