def get_system_lists():
    nomass_sys = ["Kepler-431", "LP-358-499", "Kepler-446", "EPIC-210897587-1", "EPIC-210897587-2"]
    vaneye_sys = ["K00041","K00085","K00271","K00285","K00168","K00260","K00279"]
    danjh_sys = ["KOI-0156","KOI-0152","KOI-0523","KOI-1576","KOI-0168","KOI-0085",
                 "KOI-0250","KOI-0738","KOI-2086","KOI-0115","KOI-0314","KOI-1270"]
    return nomass_sys, vaneye_sys, danjh_sys

# goes mean, upper, lower uncertainties
# units of M_sun
def get_Ms():
    Ms = {};
    Ms["KOI-0156"] = (0.56, 0, 0);              Ms["KOI-0168"] = (1.11, 0, 0);     Ms["KOI-2086"] = (1.04, 0, 0);
    Ms["KOI-1576"] = (0.907, 0, 0);             Ms["KOI-0085"] = (1.25, 0, 0);     Ms["KOI-0115"] = (0.961, 0, 0);
    Ms["KOI-0152"] = (1.165, 0, 0);             Ms["KOI-0250"] = (0.544, 0, 0);    Ms["KOI-0314"] = (0.521, 0, 0);
    Ms["KOI-0523"] = (1.07, 0, 0);              Ms["KOI-0738"] = (0.979, 0, 0);    Ms["KOI-1270"] = (0.83, 0, 0);
    Ms["Kepler-431"] = (1.071, 0, 0);   Ms["LP-358-499"] = (0.51, 0, 0);   Ms["Kepler-446"] = (0.22, 0, 0);
    #Ms["Kepler-431"] = (1.071, 0.059, 0.037);   Ms["LP-358-499"] = (0.51, 0.03, 0.03);   Ms["Kepler-446"] = (0.22, 0.05, 0.05);
    Ms["EPIC-210897587-1"] = (0.65,0.06,0.03);  Ms["EPIC-210897587-2"] = (0.540, 0.056, 0.056);
    Ms["K00041"] = (1.1093, 0.02, 0.02);        Ms["K00085"] = (1.1994,0.03,0.0301);    Ms["K00168"] = (1.078, 0.077, 0.077)
    Ms["K00260"] = (1.148, 0.051, 0.049);       Ms["K00271"] = (1.24, 0.086, 0.086);    Ms["K00279"] = (1.346, 0.084, 0.084)
    Ms["K00285"] = (1.2092, 0.02, 0.03);
    return Ms

# units of R_sun, taken from NASA exoplanet archive
def get_Rs(system):
    Rs = {}
    Rs["Kepler-431"] = 1.092;       Rs["Kepler-446"] = 0.24;        Rs["LP-358-499"] = 0.47;
    Rs["KOI-0085"] = 1.410;         Rs["KOI-0115"] = 0.894;         Rs["KOI-0152"] = 1.302;
    Rs["KOI-0156"] = 0.667;         Rs["KOI-0168"] = 1.548;         Rs["KOI-0250"] = 0.512;
    Rs["KOI-0314"] = 0.442;         Rs["KOI-1576"] = 0.814;         Rs["KOI-2086"] = 1.257;
    return Rs[system]

# goes mean, upper, lower uncertainties
# units of earth radii
def get_rad_and_period():
    #(radius, 1-sig uncertainty) pairs in earth radii for systems with no masses
    rad = {}
    rad["Kepler-431"] = ((0.77,0.16,0.14),(0.76,0.17,0.13),(1.08,0.22,0.19))
    rad["LP-358-499"] = ((1.31,0.08,0.08),(1.48,0.09,0.09),(2.02,0.13,0.13))
    rad["LP-358-499-4P"] = ((1.31,0.08,0.08),(1.48,0.09,0.09),(2.02,0.13,0.13),(1.91,0.12,0.12))
    rad["Kepler-446"] = ((1.50,0.25,0.25),(1.11,0.18,0.18),(1.35,0.22,0.22))
    rad["EPIC-210897587-1"] = ((1.8,0.20,0.1),(2.6,0.7,0.2),(1.9,0.7,0.2))          # Alonso et al.
    rad["EPIC-210897587-2"] = ((1.55,0.20,0.17),(1.95,0.27,0.22),(1.64,0.18,0.17))  # Hirano et al.

    #periods for systems with no masses, units of days
    period = {}
    period["Kepler-431"] = (6.803, 8.703, 11.922)
    period["LP-358-499"] = (3.0712, 4.8682, 11.0235)
    period["LP-358-499-4P"] = (3.0712, 4.8682, 11.0235, 26.5837)
    period["Kepler-446"] = (1.565409, 3.036179, 5.148921)
    period["EPIC-210897587-1"] = (6.342, 13.85, 40.718)
    period["EPIC-210897587-2"] = (6.34365, 13.85402, 40.6835)

    return rad, period
