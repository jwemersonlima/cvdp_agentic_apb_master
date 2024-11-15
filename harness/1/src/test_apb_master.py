import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, Timer
import harness_library as hrs_lb

@cocotb.test()
async def test_apb_master_0(dut):
   cocotb.start_soon(Clock(dut.PCLK, 10, units='ns').start())
    
   # Initialize DUT
   await hrs_lb.dut_init(dut) 
   await hrs_lb.reset_dut(dut.PRESETn)
   
   await RisingEdge(dut.PCLK)
   dut.Transfer.value = 1
   dut.PREADY.value = 1 

   for i in range(4):
      await RisingEdge(dut.PCLK)
      # Cycles 0 and 1 move the FSM to ENABLE state
      # Cycle 2 PENABLE should be 1 for 1 cycle
      # Cycle 3, PENABLE should be 0 (Pulse 1 -> 0)
      if i==0 or i==1 or i==3: 
         assert dut.PENABLE.value == 0
      elif i==2:
         assert dut.PENABLE.value == 1

      cocotb.log.info(f'[CHECK] {dut.PENABLE.value}')