module dump();
    initial begin
        $dumpfile ("wm.vcd");
        $dumpvars (0, weight_memory);


        $dumpvars (0, weight_memory.memory[0]);
        $dumpvars (0, weight_memory.memory[1]);
        $dumpvars (0, weight_memory.memory[2]);
        $dumpvars (0, weight_memory.memory[3]);

        // these are just to ensure that the memory doesnt go here
        $dumpvars (0, weight_memory.memory[4]);
        $dumpvars (0, weight_memory.memory[5]);
        #1;
    end
endmodule
