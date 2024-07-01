`timescale 1ns / 1ns

module tb;
  // Inputs
  reg clk;
  reg reset;

  // Instantiate the top level module
  tpu uut (
    .clk(clk),
    .reset(reset)
  );

  // Clock generation
  // initial begin
  //   clk = 0;
  //   forever #5 clk = ~clk; // 10ns period, 100MHz clock
  // end

  // // Simulation starts HERE
  // initial begin
  //   // Initialize inputs
  //   reset = 1;
  //   #10;
  //   reset = 0;
  // end
endmodule
