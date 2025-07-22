// I/O shield for X

// based on blank_v01
translate([-3.5, -3.5, 0]) union() {
    
    // border
    translate([2, 2, 1]){
        difference() {
            cube([158, 44, 2.58]);
            translate([1.5, 1.5, -0.01]) cube([155, 41, 2.60]);
        }
    }
    
    // backplate
    difference() {
        cube([162, 48, 1]);
        
        translate([3.5, 3.5, -1]) {
            //Place your IO recesses here.
            // PS/2 + 2 USB
            translate([5, 3, 0]) cube([15, 30, 3]);
            // DVI
            translate([5+15+18.5, 3, 0]) cube([37.5, 10, 3]);
            // VGA
            translate([5+15+22, 23, 0]) cube([30, 12, 3]);
            // HDMI + DisplayPort
            translate([5+15+58.5, 3, 0]) cube([18.5, 20, 3]);
            // USB Type-C + USB
            translate([5+15+83, 3, 0]) cube([13.5, 16, 3]);
            // 2 USB + Ethernet + 3 Audio
            translate([5+15+103, 3, 0]) cube([33, 31, 3]);
        }
    } 
}
