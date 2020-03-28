% cmpNDFDvsNOAA
close all
% % 9/11/2017 at 0900 from NOAA
%url1 = 'https://www.nhc.noaa.gov/archive/2017/al11/al112017.fstadv.049.shtml?';
% 9/11/2017 at 0600 and 1200 from NDFD
%pws0600 = '201709110600_probwindspd64i.csv';
%pws1200 = '201709111200_probwindspd64i.csv';

%NDFDvsNOAA(pws0600,pws1200,url1)

% ref time 09/10 - 0000 UTC

url3 = 'https://www.nhc.noaa.gov/archive/2017/al11/al112017.wndprb.045.shtml?';

url4 = 'https://www.nhc.noaa.gov/archive/2017/al11/al112017.wndprb.044.shtml?';

pws0600 = '201709100600_probwindspd64i_ref09100000.csv';
pws1200 = '201709101800_probwindspd64i_ref09100000.csv';

NDFDvsNOAA(url4)

% ref time 09/09 - 1800 UTC
% pws0600 = '201709100600_probwindspd64i_ref09091800.csv';
% pws1200 = '201709101200_probwindspd64i_ref09091800.csv';

% NDFDvsNOAA(pws0600,pws1200,url2)

% ref time 09/09 - 1200 UTC
% pws0600 = '201709100600_probwindspd64i_ref09091200.csv';
% pws1200 = '201709101200_probwindspd64i_ref09091200.csv';
% 
% % NDFDvsNOAA(pws0600,pws1200,url2)
% 
% % ref time 09/09 - 0600 UTC
% pws0600 = '201709100600_probwindspd64i_ref09090600.csv';
% pws1200 = '201709101200_probwindspd64i_ref09090600.csv';
% 
% % NDFDvsNOAA(pws0600,pws1200,url2)
% 
% % ref time 09/09 - 0000 UTC
% pws0600 = '201709100600_probwindspd64i_ref09090000.csv';
% pws1200 = '201709101200_probwindspd64i_ref09090000.csv';



% make movie from plots
v = VideoWriter('NDFDforecasts.avi','Uncompressed AVI');
open(v)
for j = 1:2
A = imread('33hours.jpg');
for i = 1:100
writeVideo(v,A)
end
A = imread('27hours.jpg');
for i = 1:100
writeVideo(v,A)
end
A = imread('21hours.jpg');
for i = 1:100
writeVideo(v,A)
end
A = imread('15hours.jpg');
for i = 1:100
writeVideo(v,A)
end
A = imread('9hours.jpg');
for i = 1:100
writeVideo(v,A)
end
end
close(v)
