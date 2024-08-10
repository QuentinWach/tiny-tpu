`default_nettype none
`timescale 1ns/1ns

module dma ( 
    // INPUTS
    input clk, 
    input reset, 
    input wire [7:0] uio_in, 
    // OUTPUTS
    output wire fetch_w,
    output wire fetch_inp,
    output wire fetch_ins,
    output wire start,
    output wire [3:0] dma_address
);

    // Combinational logic for outputs
    assign fetch_w = (uio_in[7:5] == 3'b001) ? 1 : 0;
    assign fetch_inp = (uio_in[7:5] == 3'b010) ? 1 : 0;
    assign fetch_ins = (uio_in[7:5] == 3'b011) ? 1 : 0;  
    assign start = (uio_in[7:5] == 3'b100) ? 1 : 0;   
    assign dma_address = uio_in[3:0];

endmodule
