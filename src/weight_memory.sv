`default_nettype none
`timescale 1ns/1ns

module weight_memory (
  input wire fetch_w, 
  input wire [7:0] ui_in, 
  input wire [3:0] dma_address,

  input wire clk,
  input wire reset,
  input wire load_weight, 
  input wire [4:0] addr, // 5 bit address but only need 3 of those bits to address 8 cells. 
  output reg [7:0] weight1,
  output reg [7:0] weight2,
  output reg [7:0] weight3,
  output reg [7:0] weight4
);
  reg [7:0] memory [0:7]; // Simple memory to store weights (only 8 addresses)
  integer i;
 
  always @(posedge clk or posedge reset) begin
    if (reset) begin
      for (i = 0; i < 8; i++) begin
        memory[i] <= 8'b0;
      end
      weight1 <= 8'b0;
      weight2 <= 8'b0;
      weight3 <= 8'b0;
      weight4 <= 8'b0;

    end else if (fetch_w) begin // READ data into weight memory 
      memory[dma_address] <= ui_in;

    end else if (load_weight) begin // WRITE weight data from weight memory into mmu processing elements, concurrently. 
      weight1 <= memory[addr];
      weight2 <= memory[addr + 1];
      weight3 <= memory[addr + 2];
      weight4 <= memory[addr + 3];

    end 
  end
endmodule
