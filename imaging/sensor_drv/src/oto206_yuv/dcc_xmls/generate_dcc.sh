DCC_TOOL_PATH=../../../../tools/dcc_tools/
OUT_PATH=../../../include

rm *.bin
rm $OUT_PATH/dcc_ldc_oto206.h
$DCC_TOOL_PATH/dcc_gen_linux oto206_ldc.xml
cat *.bin > ../dcc_bins/dcc_ldc.bin
$DCC_TOOL_PATH/dcc_bin2c ../dcc_bins/dcc_ldc.bin $OUT_PATH/dcc_ldc_oto206.h dcc_ldc_oto206

rm *.bin
