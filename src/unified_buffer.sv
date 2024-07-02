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

  // Internal counter to keep track of the next free memory location
  reg [5:0] write_pointer;

  // Initialize local variables
  integer i;

  always @(posedge clk or posedge reset) begin
    if (reset) begin
      // Initialize memory and outputs on reset
      for (i = 0; i < 64; i = i + 1) begin
        unified_mem[i] <= 0;
      end
      
      write_pointer <= 0;

      out_ub_00 <= 0; 
      out_ub_01 <= 0;
      out_ub_10 <= 0;
      out_ub_11 <= 0; 

      // Dummy activation values
      // unified_mem[16'h001E] <= 11;
      // unified_mem[16'h001F] <= 12;
      // unified_mem[16'h0020] <= 21;
      // unified_mem[16'h0021] <= 22;
    end else begin
      // Handle data coming from accumulators that is going into unified buffer
      if (store && store_acc1 && store_acc2) begin
        unified_mem[addr] <= acc1_mem_0;
        unified_mem[addr + 1] <= acc1_mem_1;
        unified_mem[addr + 2] <= acc2_mem_0;
        unified_mem[addr + 3] <= acc2_mem_1;
        write_pointer <= addr + 4;
      end
      
      // Handle loading data from unified buffer to input setup buffer
      if (load_input) begin
        out_ub_00 <= unified_mem[addr]; 
        out_ub_01 <= unified_mem[addr + 1]; 
        out_ub_10 <= unified_mem[addr + 2]; 
        out_ub_11 <= unified_mem[addr + 3]; 
      end
    end
  end

endmodule
