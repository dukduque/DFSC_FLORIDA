function psurgedat(pathtocsv)
%psurgedat creating a psruge file for the southeast region
%   This function breaks the storm file for the entire US into only that of
%   the southeast region

% Writing csv file for storm surge data
%fnames1 = fullfile('C:\','ndfd','degrib','output','testfiles','201709101200_probwindspd34c.csv');
% 'C:\ndfd\degrib\output\psurge'
% probability of storm surge >= 10 ft (3.05 meters)
pss(:,1) = csvread(pathtocsv,1,4);

% latitude and longitude of NDFD data
lat1 = csvread(pathtocsv,1,2,[1 2 length(pss(:,1)) 2]);
lon1 = csvread(pathtocsv,1,3,[1 3 length(pss(:,1)) 3]);

% Southeast		
% lower left	-90.897	24.078
% upper left	-90.570	33.181
% upper right	-77.588	32.299
% lower right	-78.861	23.253
fourcorners = [ -77.588      32.299;... % NE corner (upper right)
                -78.861      23.253;... % SE corner (lower right)
                -90.897      24.078;... % SW corner (lower left)
                -90.570      33.181];   % NW corner (lower left)

in = inpolygon(lon1,lat1,fourcorners(:,1),fourcorners(:,2));
    found = find(in);
    Latitude = lat1(in);
    Longitude = lon1(in);
    
    csvwrite('newpsurge.dat',Latitude,0,0)
    csvwrite('newpsurge.dat',Longitude,0,1)
    csvwrite('newpsurge.dat',pss,0,2)
    
end
