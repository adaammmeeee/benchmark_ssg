dtmc

module M

s:[0..5];

[] s=0 -> 0.5:(s'=1) + 0.5:(s'=3);
[] s=1 -> 0.5:(s'=0) + 0.25:(s'=2) + 0.25:(s'=4);
[r] s=2 -> 1:(s'=5);
[] s=3 -> 1:(s'=3);
[] s=4 -> 1:(s'=4);
[] s=5 -> 1:(s'=2);

endmodule

rewards "time"
true : 1;
endrewards

rewards "r"
s=4 : 3;
[r] true : 17;
endrewards
