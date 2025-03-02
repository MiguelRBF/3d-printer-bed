
M201 X500 Y500 Z100 E5000 ; sets maximum accelerations, mm/sec^2
M203 X500 Y500 Z10 E60 ; sets maximum feedrates, mm / sec
M204 S500 T1000 ; sets acceleration (S) and retract acceleration (R), mm/sec^2
M205 X8.00 Y8.00 Z0.40 E5.00 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec

M140 S50 ; set final bed temp
M106 ; turn on fan to max speed

G90 ; set absolute positioning
G28 ; Home all axes

; G92 X10 Y5; Apply a bias to all subsequent moves. To point towards the comparer clock

G1 Z22 F240 ; Move to a safe height

; ------------Start of line 1 ------------

; Point 1
G1 X45 Y50 F800 ; move to the point
G1 Z16 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z22 F240; Move to a safe height

G91 ; set relative positioning

; Point 2
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 3
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 4
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 5
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 6
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 7
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 8
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 9
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 10
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 11
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 12
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 13
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 14
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 15
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 16
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 17
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 18
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 19
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; Point 20
G1 X10 Y0 F800 ; move to the point
G1 Z-6 F240 ; move down to touch the plate
G4 P2000 ; pause 2000 ms (2s)
G1 Z6 F240; Move to a safe height

; ------------Start of line 2 ------------


; ------------End of lines ------------

G90 ; set absolute positioning

; Point 0
G1 X10 Y10 F800 ; move to the point

; M140 S0 ; turn off heatbed
; M107 ; turn off fan

M84 X Y E ; disable motors