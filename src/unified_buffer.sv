module unified_buffer (
  input clk,
  input reset,

  input store_acc1, // full flag from accumulator 1
  input store_acc2, // full flag from accumulator 2

  input [12:0] addr, // address i want to input to
  input load_input, // flag for loading input from own memory to input_setup buffer
  input store, // flag for storing data from accumulators to unified buffer

  input [31:0] acc1_mem_0,
  input [31:0] acc1_mem_1,
  input [31:0] acc2_mem_0,
  input [31:0] acc2_mem_1,

  output reg [31:0] out_ub_00,
  output reg [31:0] out_ub_01,
  output reg [31:0] out_ub_10,
  output reg [31:0] out_ub_11
);

  // the local memory
  reg [31:0] unified_mem [0:63];

  // Initialize local variables
  integer i;

  always @(posedge clk) begin
    if (reset) begin
      // Initialize memory and outputs on reset
      for (i = 0; i < 64; i = i + 1) begin
        unified_mem[i] <= 0;
      end

      out_ub_00 <= 0; 
      out_ub_01 <= 0;
      out_ub_10 <= 0;
      out_ub_11 <= 0; 

    end else if (store && store_acc1 && store_acc2) begin
      // Handle data coming from accumulators that is going into unified buffer
      unified_mem[addr] <= acc1_mem_0;
      unified_mem[addr + 1] <= acc1_mem_1;
      unified_mem[addr + 2] <= acc2_mem_0;
      unified_mem[addr + 3] <= acc2_mem_1;

    end else if (load_input) begin
      // Handle loading data from unified buffer to input setup buffer
      out_ub_00 <= unified_mem[addr]; 
      out_ub_01 <= unified_mem[addr + 1]; 
      out_ub_10 <= unified_mem[addr + 2]; 
      out_ub_11 <= unified_mem[addr + 3]; 
    end
  end

endmodule
