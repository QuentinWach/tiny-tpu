/* Generated by Yosys 0.36+67 (git sha1 1ddb0892c, aarch64-apple-darwin20.2-clang 10.0.0-4ubuntu1 -fPIC -Os) */

(* top =  1  *)
(* src = "control_unit.sv:4.1-110.10" *)
module control_unit(clk, reset, start, base_address, load_input, load_weight, valid, store, ext);
  (* src = "control_unit.sv:37.3-62.8" *)
  wire _0_;
  (* src = "control_unit.sv:8.21-8.33" *)
  output [12:0] base_address;
  wire [12:0] base_address;
  (* src = "control_unit.sv:5.14-5.17" *)
  input clk;
  wire clk;
  (* src = "control_unit.sv:13.14-13.17" *)
  output ext;
  wire ext;
  (* src = "control_unit.sv:31.14-31.25" *)
  wire [15:0] instruction;
  (* src = "control_unit.sv:9.14-9.24" *)
  output load_input;
  wire load_input;
  (* src = "control_unit.sv:10.14-10.25" *)
  output load_weight;
  wire load_weight;
  (* src = "control_unit.sv:6.14-6.19" *)
  input reset;
  wire reset;
  (* src = "control_unit.sv:7.14-7.19" *)
  input start;
  wire start;
  (* src = "control_unit.sv:12.14-12.19" *)
  output store;
  wire store;
  (* src = "control_unit.sv:11.14-11.19" *)
  output valid;
  reg valid;
  assign _0_ = ~reset;
  (* src = "control_unit.sv:37.3-62.8" *)
  always @*
    if (reset) valid = _0_;
  assign base_address = 13'h0000;
  assign ext = 1'h0;
  assign instruction = 16'h0000;
  assign load_input = 1'h0;
  assign load_weight = 1'h0;
  assign store = valid;
endmodule
