% % 9/10/2017 at 0900 from NOAA
clear all
close all

url = 'https://www.nhc.noaa.gov/archive/2017/al11/al112017.fstadv.049.shtml?';


urls = [ 'https://www.nhc.noaa.gov/archive/2017/al11/al112017.fstadv.047.shtml?' ...
        'https://www.nhc.noaa.gov/archive/2017/al11/al112017.fstadv.048.shtml?'...
        'https://www.nhc.noaa.gov/archive/2017/al11/al112017.fstadv.049.shtml?']
    
fnamess = [fullfile('C:\ndfd\degrib\output\testfiles\20170911\i_LE\201709111200_probwindspd64i.csv');...
           fullfile('C:\ndfd\degrib\output\testfiles\20170911\i_LE\201709111200_probwindspd64i.csv'); ...
           fullfile('C:\ndfd\degrib\output\testfiles\20170911\i_LE\201709111200_probwindspd64i.csv');]

fnames = fullfile('C:\ndfd\degrib\output\testfiles\20170911\i_LE\201709110600_probwindspd64i.csv');       
fnames2 = fullfile('C:\ndfd\degrib\output\testfiles\20170911\i_LE\201709111200_probwindspd64i.csv');

wprob(:,1) = csvread(fnames,1,4);
wprob2(:,2) = csvread(fnames2,1,4);

lat = csvread(fnames,1,2,[1 2 length(wprob(:,1)) 2]);
lon = csvread(fnames,1,3,[1 3 length(wprob(:,1)) 3]);

% extract the NOAA data from webpage
html = urlread(url);
% Use regular expressions to remove undesired markup.
txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');
centerindex = strfind(txt, 'HURRICANE CENTER LOCATED NEAR ');
centerindex = centerindex + strlength('HURRICANE CENTER LOCATED NEAR ');

% AT 0300Z THE CENTER OF HURRICANE IRMA WAS LOCATED NEAR LATITUDE 23.5
% NORTH...LONGITUDE 81.0 WEST WITH MAXIMUM SUSTAINED WINDS NEAR 105
% KTS...120 MPH...195 KM/H.
latcent = str2num(txt(centerindex:centerindex+3));
lat_dir = txt(centerindex+4);
loncent = str2num(txt(centerindex+7:centerindex+10));
lon_dir = txt(centerindex+11);

if lat_dir == 'S'
    latcent = latcent*(-1);
end
if lon_dir == 'W'
    loncent = loncent*(-1);
end

% based off the following format
% 64 KT.......  0NE   0SE  50SW  50NW.
% 50 KT.......140NE 140SE  90SW 120NW.
% 34 KT.......360NE 230SE 150SW 240NW.
% 12 FT SEAS..470NE 270SE 480SW 360NW.
rangesindex = strfind(txt,'64 KT.......');
rangesindex = rangesindex + strlength('64 KT.......');
NE = str2num(txt(rangesindex:rangesindex+2));
SE = str2num(txt(rangesindex+6:rangesindex+8));
SW = str2num(txt(rangesindex+12:rangesindex+14));
NW = str2num(txt(rangesindex+18:rangesindex+20));

% create the NOAA polygon
% NOTE** -> One minute of latitude equals one nautical mile
%                              LAT                  LON
fourcorners = (1/60)*[     (sind(45)*NE)      (cosd(45)*NE);... % NE corner
                        -1*(sind(45)*SE)      (cosd(45)*SE);... % SE corner
                        -1*(sind(45)*SW)   -1*(cosd(45)*SW);... % SW corner
                           (sind(45)*NW)   -1*(cosd(45)*NW)];   % NW corner

fourcorners = [(latcent + fourcorners(:,1)), (loncent + fourcorners(:,2))];

% in = inpolygon(xq,yq,xv,yv)
in = inpolygon(lon,lat,fourcorners(:,2),fourcorners(:,1));
found = find(in);

lat_in = lat(in);
lon_in = lon(in);

%Interpolate in time between 0600 and 1200 to find an NDFD proxy for 0900
wprob_inter = mean([wprob(in) wprob(in)],2);

figure()
%clear NOAApws1
%NOAApws1(1:length(lat_in),1) = NOAApws_cu(ii);
scatter3(lon_in,lat_in,wprob_inter,[],wprob_inter,'o','filled')
hold on

xlabel('longitude')
ylabel('latitude')
zlabel('Probability of Wind at/above 64 kts')
%legend('NDFD data','NOAA data')
title('9/11 0900 Incremental PWS >= 64 kts in NOAA Quadrant')
%zlim([0 100])
%view([-180 90])
view([-45 4])
colorbar
