# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

# i think i want to make it so that it only fetches when a flag is high
@cocotb.test() 
async def test_wm(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    dut.reset.value = 0

    await ClockCycles(dut.clk, 1)
    
    dut.reset.value = 1
    await ClockCycles(dut.clk, 1)

    dut.reset.value = 0
    await ClockCycles(dut.clk, 1)

    dut.reset.value = 0
    await ClockCycles(dut.clk, 1) 

    # These two lines below are decoded from uio_in in the dma module
    dut.fetch_w.value = 1 # accept inputs into weight memory
    dut.dma_address = 0b0000 # input into address #1
    # Input from ui_in 
    dut.ui_in.value = 0b00000011  # load weight 3
    await ClockCycles(dut.clk, 1)
    
    dut.fetch_w.value = 1 # accept inputs into weight memory
    dut.dma_address = 0b0001 # input into address #2
    dut.ui_in.value = 0b00000100  # load weight 4
    await ClockCycles(dut.clk, 1)

    dut.fetch_w.value = 1 # accept inputs into weight memory
    dut.dma_address = 0b0010 # input into address #3
    dut.ui_in.value = 0b00000101 # load weight 5
    await ClockCycles(dut.clk, 1)

    dut.fetch_w.value = 1 # accept inputs into weight memory
    dut.dma_address = 0b0011 # input into address #4
    dut.ui_in.value = 0b00000110 # load weight 6
    await ClockCycles(dut.clk, 1)

    dut.fetch_w.value = 0 # DONT ACCEPT ANYTHING!!!!!!!!!!!!!!!!!!!!!!!
    dut.dma_address = 0b0011 # input into address #4
    dut.ui_in.value = 0b00000110 # load weight 6
    await ClockCycles(dut.clk, 1)
    await ClockCycles(dut.clk, 1)
    await ClockCycles(dut.clk, 1)
    # ^^^ lines 46-49 SHOULD NOT AFFECT THE MEMORY CONTENTS

