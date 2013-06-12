import HSTP.SetHSTPPath
import os, sys
PathToApp = os.path.split(HSTP.SetHSTPPath.__file__)[0]+"/Pydro/" 
os.environ['PathToPydro']=PathToApp
HSTP.SetHSTPPath.AddAll()

import scipy
import numpy as np

import Profile
import Seacat
import VelocConstants
import scipy.interpolate
import matplotlib as mpl
import matplotlib.pyplot as plt

def sv_import(filename, lat, ret_full = False):
    '''Returns an array of valid sound speed points for depths recorded by
    the CTD in a CNV file.  Not averaged.
    ss = sv_compare.sv_import("2013_074_193613.cnv", 44.626)
    '''
    if filename[-4:] == 'calc':
        #MVP file
        try:
            cast_data = Profile.ScipyProfile.parseRawProfile(filename)[0]
        except Exception, e:
            print "Error: ", e
            return
        binsz = 0.1
        return cast_data.QC(bin=(cast_data.dtype.names, binsz))
    elif filename[-3:] == 'cnv': 
        #CTD file
        try:
            cnv_data = Profile.ScipyProfile.parseRawProfile(filename)[0]
        except Exception, e:
            print "Error: ", e
            return
        
        cnv_name = cnv_data.metadata['Filename']
        sthresh, Pmax, Nvalues, interval = Seacat.GetThresh(cnv_data)
        Z0, in_air_data, in_water_data = Seacat.GetOffset(cnv_data, sthresh, 
            parent = None) #' Using the salinity threshold, compute pressure offset.
        in_water_data = scipy.compress(in_water_data['salinity']<=40, in_water_data) #ignore if Salinity out-of-bounds
        if len(in_water_data)>0: # ' instrument in water?
            IMAX = in_water_data['pressure'].argmax() #index of end of down cast
            upcast = False
            if upcast:
                in_water_data = in_water_data[IMAX:]
            else:
                in_water_data = in_water_data[:IMAX+1]
                
            Sthresh2 = 0.8 * in_water_data['salinity'][0] #Mod 3/19/96 - use of Sthresh2 to handle case where instrument comes up out of water.
            in_water_data = scipy.compress(in_water_data['salinity']>Sthresh2,
                in_water_data)
            in_water_data['pressure']-=Z0 #' Corrected pressure
            in_water_data = scipy.compress(in_water_data['pressure']>-0.001,
                in_water_data) #Ignore data in air (corrected pressure<0)
                
            '''
            # Averaging not desired in this case
            if IDiverFlag:
                binsize, binwidth = 0.1, 5
                WWmin, WWMul = 0.3, .025
            else:
                binsize, binwidth = 1.0, 4
                WWmin, WWMul = 1.7, .0025
            fields = list(in_water_data.dtype.names)
            try: fields.remove('flag')
            except: pass #didn't have flag??
            avg_data = Profile.CosineAvg(in_water_data, fields, binsize, binwidth, WWmin, WWMul)
            '''
            
            avg_data = in_water_data

            ddens = scipy.hstack(([0],scipy.diff(avg_data['density'])))
            G = 978.0318 * (1.0 + 0.0053024 
                * (scipy.sin(lat*VelocConstants.DEG2RAD()) ** 2) - 0.0000059 
                * (scipy.sin(2 * lat*VelocConstants.DEG2RAD()) ** 2))
            Gj = (G + 0.0001113 * avg_data['pressure']) * 0.001
            Dj = (1000 + avg_data['density']) * 0.001
            depths = scipy.zeros([len(Dj)])
            for i in range(len(Dj)):
                if i>0:
                    depths[i] =  depths[i - 1] + (avg_data['pressure'][i] - 
                        avg_data['pressure'][i - 1]) / (Dj[i] * Gj[i])
                else: 
                    depths[0] =  0 + (avg_data['pressure'][0] - 0) / (Dj[0] * Gj[0])
            
            ''' *************************************************************
            ' The following segment derives from days of EEZ. Retain it.
            ' Force the first 99 levels and last level to be significant.
            ' Flag "significant" by making pressure negative.
            '''
            significant = scipy.zeros([len(depths)], scipy.int8)
            significant[:100]+=1
            significant[-1] = 1
            sspeed = avg_data['soundspeed']
            J = 100
            #' Begin loop to determine remaining significant levels
            while J<len(depths):
                Ia = 1 + int(0.5 + J * 0.005); K = Ia * 2
                LN = J + K
                level_data = sspeed[J:LN]
                Jmax = scipy.argmax(level_data)
                Jmin = scipy.argmin(level_data)
                significant[J + Jmin]=1 #remember, we're looking at the sub-slice so we adjust the absolute index.
                significant[J + Jmax]=1
                J = J + Ia
            newdata = Profile.ScipyProfile(avg_data, **cnv_data.get_keyargs())
            newdata = newdata.append_field('depth', depths) #cnv_data -- metadata
            newdata.SetYMetricName('depth')
            final_prof = Profile.ScipyProfile(newdata.compress(significant>0), 
                **newdata.get_keyargs())

            #create histogram to determine low depth cutoff
            hist = np.histogram(final_prof['depth'], 
                np.arange(np.floor(final_prof['depth'].min()), 
                np.ceil(final_prof['depth'].max()), 0.5))
            #min_depth = np.ma.masked_where(hist[0] > 10 , hist[1][:-1]).min()
            min_depth = hist[1][hist[0].argmax() + 1]
            #print "Min Depth: %.1f" % min_depth
            
            valid_depths = final_prof['depth'] >= min_depth
            if ret_full:
                return Profile.ScipyProfile(final_prof.compress(valid_depths), 
                    **final_prof.get_keyargs())
            else:
                return scipy.vstack((final_prof['depth'].compress(valid_depths), 
                    final_prof['soundspeed'].compress(valid_depths)))
        else:
            print "Instrument not in water"
    else:
        print 'Format unrecognised.'

def get_data_only(profile):
    return scipy.vstack((profile['depth'], 
        profile['soundspeed']))
        
def compare_casts(cast_ref, cast_comp):
    '''Expects casts to be in condensed form: array with cast[0] = depth,
    cast[1] = sound speed
    Outputs comparison metrics of comparison cast interpolated to depths
    in the reference cast.
    '''
    # Fill these out to define the colors being compared
    ref_color_str = 'Purple'
    comp_color_str = 'Black'
    
    interpf = scipy.interpolate.interp1d(cast_comp[0], cast_comp[1])
    cast_ref_depths = np.logical_and(cast_ref[0] >= np.min(cast_comp[0]), 
        cast_ref[0] <= np.max(cast_comp[0]))
    #min depth limit:
    #cast_ref_depths = np.logical_and(cast_ref[0] >= np.min(cast_comp[0]), 
    #    cast_ref[0] <= np.max(cast_comp[0]))
    comp_vals = interpf(cast_ref[0][cast_ref_depths])
    diffs = cast_ref[1][cast_ref_depths] - comp_vals
    #print diffs
    print '\n====================================='
    print ' Sound Speed Cast Comparison Results'
    print '====================================='
    print '%i Values Compared' % len(diffs)
    print 'Max Absolute Difference: %0.3f' % np.max(np.abs(diffs))
    print 'Average Difference: %0.3f' % np.mean(diffs)
    print 'Average Absolute Difference: %0.3f' % np.mean(np.abs(diffs))
    print 'StDev Differences: %0.3f' % np.std(diffs)
    
    #plot the data
    ref_color = get_plot_color(ref_color_str)
    comp_color = get_plot_color(comp_color_str)
    plt.plot(cast_ref[1,cast_ref_depths], cast_ref[0,cast_ref_depths], 
        c=ref_color, marker='s', label='Reference Cast', linewidth=2, mew=0, 
        ms=8)
    plt.hold(True)
    plt.plot(cast_comp[1], cast_comp[0], c=comp_color, marker='D', 
        label='Comparison Cast', linewidth=2, mew=0)
    plt.plot(comp_vals, cast_ref[0,cast_ref_depths], c=comp_color, marker='o', 
        label='Comparison Points', linewidth=2, ls='None', mew=0)
    
    #format the plot
    plt.title('CTD Comparison: ' + comp_color_str + ' vs. ' + ref_color_str)
    plt.gca().invert_yaxis()
    plt.gca().yaxis.grid(c='0.3')
    svformat = mpl.ticker.FormatStrFormatter('%.2f')
    plt.gca().xaxis.set_major_formatter(svformat)
    plt.ylabel('Depth (m)')
    plt.xlabel('Sound Speed (m/s)')
    plt.legend(loc='best')
    plt.show()

def get_plot_color(ctd_color):
    ctd_color = ctd_color.lower()
    if ctd_color[0] == 'y':
        return (255.0/255, 192.0/255, 0)
    elif ctd_color[0] == 'p':
        return (112.0/255, 48.0/255, 160.0/255)
    elif ctd_color[0] == 'b':
        return (0, 0, 0)
    elif ctd_color[0] == 'w':
        return '0.75'
    elif ctd_color[0] == 'g':
        return (119.0/255, 147.0/255, 60.0/255)
    elif ctd_color[0] == 'm':   #MVP is now orange...
        return (255.0/255, 127.0/255, 39.0/255)
    elif ctd_color[0] == 'l':   #Launch MVP is blue...
        return (219.0/255, 238.0/255, 243.0/255)        

def main():
    if len(sys.argv) == 4:
        #Arguments = ref_cast comp_cast latitude
        lat = float(sys.argv[3])
        filename2 = sys.argv[2]
        filename1 = sys.argv[1]
        prof1 = sv_import(filename1, lat, True)
        prof2 = sv_import(filename2, lat, True)
        compare_casts(get_data_only(prof1), get_data_only(prof2))
        
        # Run velocipy DQA (beam angle based)        
        dqa = prof1.DQACompare(prof2, 64) #64 is max 7125 beam angle in degrees
        print '\n Velocipy DQA'
        print '--------------'
        print dqa[2]
        print dqa[0]
    else:
        filename = sys.argv[1]
        lat = float(sys.argv[2])
        prof = sv_import(filename, lat)
        print prof

if __name__ == '__main__':
    main()