# Failure-clip annotation notes

These labels are visual assessments of the supplied onboard-camera clips. All six
clips are most consistent with a **planner/navigation deadlock candidate**: a
barrier or fence blocks the apparent route and the camera shows little net
progress or only local reorientation.

The clips alone do not reveal the navigation goal, replanning state, frontier
selection, map-growth rate, or whether the robot is physically in contact with
an obstacle. For that reason, none is labeled as confirmed physical
immobilization, goal/frontier oscillation, or low-progress. Confirmation requires
the synchronized localization, planner, costmap, and command-velocity logs.
