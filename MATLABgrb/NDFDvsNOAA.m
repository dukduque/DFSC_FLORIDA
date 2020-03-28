function NDFDvsNOAA(url)
%NDFDVSNOAA comparing NDFD data with NOAA data
%   This function interpolates in time between the two NDFD data sets then
%   locates all the NDFD data within the designated polygon from NOAA
%   for accuracy. cent = [latcent, loncent] and ranges = [NE, SE, SW, NW]

%%% First locate the NDFD position that are within the
%%% >34kt wind quadrant/polygon defined by NOAA

% FROM NDFD
% using generated csv files from degrib/tkdegrib
fnames1 = fullfile('C:\','ndfd','degrib','output','testfiles','201709101200_probwindspd34c.csv');
fnames2 = fullfile('C:\','ndfd','degrib','output','testfiles','201709110000_probwindspd34c.csv');
fnames3 = fullfile('C:\','ndfd','degrib','output','testfiles','201709111200_probwindspd34c.csv');
fnames4 = fullfile('C:\','ndfd','degrib','output','testfiles','201709120000_probwindspd34c.csv');

% probability of wind speed >= 34 kts
pws(:,1) = csvread(fnames1,1,4);
pws(:,2) = csvread(fnames2,1,4);
pws(:,3) = csvread(fnames3,1,4);
pws(:,4) = csvread(fnames4,1,4);
% latitude and longitude of NDFD data
lat1 = csvread(fnames1,1,2,[1 2 length(pws(:,1)) 2]);
lon1 = csvread(fnames1,1,3,[1 3 length(pws(:,1)) 3]);

% probability of wind speed >= 64 kts
% pws(:,1) = table2array(NDFDt1(:,5));
% pws(:,2) = table2array(NDFDt2(:,5));
% pws(:,3) = table2array(NDFDt3(:,5));

% extract the NOAA data from webpage
html = urlread(url);
% Use regular expressions to remove undesired markup.
txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

centerindex = strfind(txt, 'WAS LOCATED NEAR LATITUDE ');
centerindex = centerindex + strlength('WAS LOCATED NEAR LATITUDE ');

% based off the following format
% HURRICANE CENTER LOCATED NEAR 27.4N 71.2W AT 16/1500Z

%Gainesville, FL ->> 29.6516° N, 82.3248° W
latcent(1) = 29.7;
loncent(1) = -82.3;

% CEDAR KEY FL 29.1386° N, 83.0351° W
latcent(2) = 29.1;
loncent(2) = -83.0;

% TALLAHASSEE FL 30.4383° N, 84.2807° W
latcent(3) = 30.4;
loncent(3) = -84.3;

% latcent(4)  = 25.7617;
% latcent(4)  = -80.1918;


% based off the following format
% 64 KT.......  0NE   0SE  50SW  50NW.
% 50 KT.......140NE 140SE  90SW 120NW.
% 34 KT.......360NE 230SE 150SW 240NW.
% 12 FT SEAS..470NE 270SE 480SW 360NW.
rangesindex = strfind(txt,'64 KT.......');
rangesindex = rangesindex + strlength('64 KT.......');
NE = str2num(txt(rangesindex:rangesindex+2)); % 50; 
SE = str2num(txt(rangesindex+6:rangesindex+8));  % 50 
SW = str2num(txt(rangesindex+12:rangesindex+14)); % 50
NW = str2num(txt(rangesindex+18:rangesindex+20)); % 50

% Read windspeed probabilities
orl_ind(1) = strfind(txt,'GAINESVILLE FL 34 ');
orl_ind(1) = orl_ind(1) + strlength('GAINESVILLE FL 34 ');

orl_ind(2) = strfind(txt,'CEDAR KEY FL   34 ');
orl_ind(2) = orl_ind(2) + strlength('CEDAR KEY FL   34 ');

orl_ind(3) = strfind(txt,'TALLAHASSEE FL 34 ');
orl_ind(3) = orl_ind(3) + strlength('TALLAHASSEE FL 34 ');
cities = [string('GAINESVILLE FL') string('CEDAR KEY FL') string('TALLAHASSEE FL')];

%for i = 1:3 % for each city
for i = 1:3
    % onset probability
    onpws(1,i) = string(txt(orl_ind(i):orl_ind(i)+1));
    onpws(2,i) = string(txt(orl_ind(i)+4:orl_ind(i)+5));
    onpws(3,i) = string(txt(orl_ind(i)+12:orl_ind(i)+13));
    onpws(4,i) = string(txt(orl_ind(i)+20:orl_ind(i)+21));
    onpws(5,i) = string(txt(orl_ind(i)+28:orl_ind(i)+29));
    onpws(6,i) = string(txt(orl_ind(i)+36:orl_ind(i)+37));
    onpws(7,i) = string(txt(orl_ind(i)+44:orl_ind(i)+45));
    
    % cumulative probability
    cupws(1,i) = string(txt(orl_ind(i)+7:orl_ind(i)+8));
    cupws(2,i) = string(txt(orl_ind(i)+15:orl_ind(i)+16));
    cupws(3,i) = string(txt(orl_ind(i)+23:orl_ind(i)+24));
    cupws(4,i) = string(txt(orl_ind(i)+31:orl_ind(i)+32));
    cupws(5,i) = string(txt(orl_ind(i)+39:orl_ind(i)+40));
    cupws(6,i) = string(txt(orl_ind(i)+47:orl_ind(i)+48));
    
    for j = 1:7 % for each probability range
        if sum(char(onpws(j,i)) == ' X') == 2
            NOAApws_on(j) = 0;
        else
            NOAApws_on(j) = str2num(char(onpws(j,i)));
        end
        if j ~= 7
            if sum(char(cupws(j,i)) == ' X') == 2
                NOAApws_cu(j) = 0;
            else
                NOAApws_cu(j) = str2num(char(cupws(j,i)));
            end
        end
    end
    
    
    % create the NOAA polygon
    % NOTE** -> One minute of latitude equals one nautical mile
    %                           LAT                  LON
    fourcorners = (1/60)*[   (sind(45)*NE)      (cosd(45)*NE);... % NE corner
                          -1*(sind(45)*SE)      (cosd(45)*SE);... % SE corner
                          -1*(sind(45)*SW)   -1*(cosd(45)*SW);... % SW corner
                             (sind(45)*NW)   -1*(cosd(45)*NW)];   % NW corner
    
    fourcorners = [(latcent(i) + fourcorners(:,1)), (loncent(i) + fourcorners(:,2))];
    
    % in = inpolygon(xq,yq,xv,yv)
    in = inpolygon(lon1,lat1,fourcorners(:,2),fourcorners(:,1));
    found = find(in);
    lat_in = lat1(in);
    lon_in = lon1(in);
    % check = lat_in(end) -  lat0600(found(end))
    % ^ from these we know latitudes and longitudes from NDFDt1 and t2 are the
    % same
    times = [string('0-12 hours') string('0-24 hours') string('0-36 hours')]
    for ii = 1:3 % for only probability ranges 1-3
        % pws1(in) vs orlpws(1)
        
        figure()
        pws1 = pws(:,ii);
        pws1 = pws1(in)
       
        clear NOAApws1
        %NOAApws1(1:length(lat_in),1) = NOAApws_cu(ii);
        scatter3(lon_in,lat_in,pws1,[],pws1,'o','filled')
        %scatter3(lon_in,lat_in,pws1,'r','filled')
        hold on
        scatter3(loncent(i),latcent(i),NOAApws_cu(ii),[],NOAApws_cu(ii),'square','filled')
        hold on
        xlabel('longitude')
        ylabel('latitude')
        zlabel('probability of wind speed at/above 34 kts')
        legend('NDFD data','NOAA data')
        title(['9/10 00Z Cumulative PWS ' char(cities(i)) ' in range ' char(times(ii))])
        zlim([0 100])
        view([-180 90])
        %view([-45 4])
        colorbar

        
    end

end

% Interpolate in time between 0600 and 1200 to find an NDFD proxy for 0900
% pws_intpol = mean([pws1(in) pws2(in)],2);

ind = strfind(NDFDn1,'_ref') + length('_ref');
ref = NDFDn1(ind:ind+8);
ref = [ref(1:2) '/' ref(3:4) ' - ' ref(5:8) ' UTC']
tit = 'PWS within NOAA 64kts quadrant ref: ';
tit = [tit ref];
scatter3(lon_in,lat_in,pws_intpol,[],pws_intpol,'filled')
xlabel('longitude')
ylabel('latitude')
zlabel('probability of wind speed at/above 64 kts')
zlim([0 100])
title(tit)
% view([-45 4])


end
