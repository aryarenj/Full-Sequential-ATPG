set_messages -log ./test_gen.log -replace
read_netlist ./mylib.v
read_netlist ./CUT_scan.v
run_build_model s13207

add_clocks 0 { CK } -shift -timing { 100 50 80 40 }
add_scan_chain chain1 SI SO
add_scan_enables 1 SE

add_nofaults -module S_DFFX1
add_nofaults -module S_DFFSRX1

add_pi_constraint 0 SI
add_pi_constraint 0 SE
add_pi_constraint 0 GND
add_pi_constraint 1 VDD

run_drc

set_faults -model stuck
remove_faults -all


add_faults -all
set_atpg -full_seq_atpg

run_atpg -ndetects  1 

report_faults -summary
write_patterns  ./ATPG_pattern.stil -exclude setup -format stil -replace
write_faults faults_list_1  -uncollapsed -all -replace
write_faults faults_left -class ND -replace

