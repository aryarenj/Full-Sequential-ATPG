set_messages -log ./fault_sim.log -replace

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

remove_faults -all
set_patterns -delete


set_patterns  -external ./Fault_Sim.pattern
set_simulation -measure sim
run_simulation -override_differences 

write_patterns ./patterns_v2.stil -exclude setup -format stil -external -replace
set_patterns -delete
set_patterns -external ./patterns_v2.stil

add_faults -all
set_atpg -full_seq_atpg

run_fault_sim

report_faults -summary
write_faults ./fault.left -class UD -class PT -class AU -class ND -replace

