This will remove the user installed version of zoom on the system.
This can be sent via SCCM to a group of PC's with this problem.
The problem I was facing was keeping the software updated system-wide. If each user has a diffrent version it made this difficult. The solution was to run this script to remove the software and let add the same PC's to a SCCM group to install the MSI system wide instead.
