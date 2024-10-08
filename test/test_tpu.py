# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles


async def inititialize_weight_memory(dut):
    dut.uio_in.value = 0b0010_0000 # fetch weight "i am holding this down!" and load into address 1
    dut.ui_in.value = 0b00000011 # load weight 3
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b0010_0001 # fetch weight "i am holding this down!" and load into address 2
    dut.ui_in.value = 0b00000100 # load weight 4
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b0010_0010 # fetch weight "i am holding this down!" and load intro address 3
    dut.ui_in.value = 0b00000101 # load weight 5
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b0010_0011 # fetch weight "i am holding this down!" and load into address 4
    dut.ui_in.value = 0b00000110 # load weight 6
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b0000_0000  # Stop fetching weights
    dut.ui_in.value = 0b00000000   # no more input
    await ClockCycles(dut.clk, 1)


async def initialize_unified_mem(dut):
    dut.uio_in.value = 0b01000011 # fetch weight and load into address 3
    dut.ui_in.value = 0b00001011 # load weight 11
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01000100 # fetch weight and load into address 4
    dut.ui_in.value = 0b00001100 # load weight 12
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01000101 # fetch weight and load intro address 5
    dut.ui_in.value = 0b00010101 # load weight 21
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01000110 # fetch weight and load into address 6
    dut.ui_in.value = 0b00010110 # load weight 22
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b0000_0000  # Stop fetching inputs
    dut.ui_in.value = 0b00000000   # no more input
    await ClockCycles(dut.clk, 1)


async def initialize_instruction_mem(dut):
    dut.uio_in.value = 0b01100000 # input instruction at address 1
    dut.ui_in.value = 0b001_00011 # LOAD_ADDR (4th address)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01100001 # input instruction at address 2
    dut.ui_in.value = 0b011_00000 # LOAD_INPUT (take input from unified buffer and transfer to input setup)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01100010 # input instruction at address 3
    dut.ui_in.value = 0b001_00000 # LOAD_ADDR (1st address)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01100011 # input instruction at address 4
    dut.ui_in.value = 0b010_00000 # LOAD_WEIGHT (Weights are transferred from weight memory into mmu)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01100100 # input instruction at address 5
    dut.ui_in.value = 0b100_00000 # COMPUTE (Weights are transferred from weight memory into mmu)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01100101 # input instruction at address 6
    dut.ui_in.value = 0b001_01000 # LOAD_ADDR (load result in 9th address)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01100110 # input instruction at address 7
    dut.ui_in.value = 0b101_00000 # STORE (result is stored in address above within unified buffer)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01100111 # input instruction at address 8
    dut.ui_in.value = 0b001_01001 # LOAD_ADDR (10th address: which means only last two product matrix elements will be outputted)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01101000 # input instruction at address 9
    dut.ui_in.value = 0b111_00000 # EXT (output data off-chip, starting from the address specified above)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b01101001 # input instruction at address 10
    dut.ui_in.value = 0b000_00000 # EXT (output data off-chip, starting from the address specified above)
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0b00000000 # stop recieving instructions
    dut.ui_in.value = 0b00000000 # EXT (output data off-chip, starting from the address specified above)
    await ClockCycles(dut.clk, 1)


@cocotb.test()
async def test_tpu(dut):
    # TODO: change dut.start to dut.uio_in = 10000000 & dut.ui_in = 0000000
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start()) # Start the clock

    dut.reset.value = 1  # Reset the DUT
    dut.uio_in = 0b00000000 # no input during reset
    dut.ui_in = 0b00000000 # no input during reset
    await ClockCycles(dut.clk, 1)

    dut.reset.value = 0
    dut.uio_in = 0b00000000 # no input during reset
    dut.ui_in = 0b00000000 # no input during reset
    await ClockCycles(dut.clk, 1)

    # DATA INITIALIZATION
    await initialize_unified_mem(dut) # Initialize inputs
    await inititialize_weight_memory(dut) # Initialize weights
    await initialize_instruction_mem(dut)  # Initialize instructions

    dut.uio_in = 0b10000000 # START (starts program)
    dut.ui_in = 0b00000000
    await ClockCycles(dut.clk, 1) 

    dut.start.value = 0  # De-assert start signal
    dut.uio_in = 0b00000000 # deassert start signal
    dut.ui_in = 0b00000000 # no input


    # ^^ uio_in ui_in now just keep asserting zero for the remaining 28 clock cycles

    #################################################
    #                                              #
    #           PROGRAM STARTS HERE!!!!!!!!!!!     #
    #                                              #
    ################################################

    for cycle in range(28):
        await RisingEdge(dut.clk)

        # Print values of the accumulators for every clock cycle in decimal
        dut._log.info(f"Cycle {cycle + 1}:")
        dut._log.info(f"acc1_mem_0 = {int(dut.acc1.acc_mem[0].value)}")
        dut._log.info(f"acc1_mem_1 = {int(dut.acc1.acc_mem[1].value)}")
        dut._log.info(f"acc2_mem_0 = {int(dut.acc2.acc_mem[0].value)}")
        dut._log.info(f"acc2_mem_1 = {int(dut.acc2.acc_mem[1].value)}")
        dut._log.info(f"-----------------------------")

    # Print all 16 values of the unified memory from unified_buffer after the loop
    for i in range(16):
        unified_mem_val = int(dut.ub.unified_mem[i].value)
        dut._log.info(f"unified_mem[{i}] = {unified_mem_val}")
    

