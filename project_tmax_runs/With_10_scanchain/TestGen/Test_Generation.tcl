set_messages -log ./test_gen.log -replace
read_netlist ./mylib.v
read_netlist ./CUT_multiple_scan.v
run_build_model s13207

add_clocks 0 { CK } -shift -timing { 100 50 80 40 }
add_scan_chain chain1 SI1 SO1
add_scan_chain chain2 SI2 SO2
add_scan_chain chain3 SI3 SO3
add_scan_chain chain4 SI4 SO4
add_scan_chain chain5 SI5 SO5
add_scan_chain chain6 SI6 SO6
add_scan_chain chain7 SI7 SO7
add_scan_chain chain8 SI8 SO8
add_scan_chain chain9 SI9 SO9
add_scan_chain chain10 SI10 SO10



add_scan_enables 1 SE

add_nofaults -module S_DFFX1
add_nofaults -module S_DFFSRX1

add_pi_constraint 0 SI1
add_pi_constraint 0 SI2
add_pi_constraint 0 SI3
add_pi_constraint 0 SI4
add_pi_constraint 0 SI5
add_pi_constraint 0 SI6
add_pi_constraint 0 SI7
add_pi_constraint 0 SI8
add_pi_constraint 0 SI9
add_pi_constraint 0 SI10

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

