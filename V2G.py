import numpy as np

def getArrivalTime(nVech, useCase):
    if useCase == 1: # residential
        arrivalTime = np.random.normal(20, 2, nVech)
        return arrivalTime
    if useCase == 2:  # office
        arrivalTime = np.random.lognormal(2.32274, 0.301833, nVech)
        return arrivalTime
    if useCase == 3: # commercial
        Charge_Freq = [507.377049200000, 422.885245900000, 401.639344300000, 420.262295100000, 508.688524600000,
                        634.918032800000, 898.52459000000, 1390.57377000000, 1913.80327900000, 2187.81967200000,
                        2363.32786900000, 2139.70491800000, 1821.21511500000, 1335.36065600000, 1311.39344300000,
                        603.377049180328]
        values = [0.097654718, 1.146678171, 3.221429132, 5.887402934, 7.3409287, 9.046121264, 10.92744529, 13.06608361,
                  15.9770178100000, 18.0320025100000, 19.7054278800000, 21.7332339800000, 22.5238842300000,
                  23.1479331700000, 23.8559887000000, 24.0976547180171]
        values_new = range(1440)
        Charge_Prob_new2 = user_definedProb(Charge_Freq, values)
        arrivalTime = np.random.choice(values_new, nVech, p=list(Charge_Prob_new2))
        return arrivalTime/60
    if useCase == 4: # public
        Charge_Freq = [377.049180300000, 407.065573800000, 439.491803300000, 502.68852500000,
                       557.18032800000, 664.37704900000, 874.91803300000, 1109.42623000000, 1773.93442600000,
                       1974.59016400000, 2073.77049200000, 2098.36065600000, 2110.65573800000, 2116.80327900000,
                       2104.50819700000, 2086.06557400000, 2079.91803300000, 2055.32786900000, 1944.67213100000,
                       1840.16393400000, 1704.91803300000, 1606.55737700000, 1508.19672100000, 1348.36065600000,
                       1225.40983600000, 1108.60655700000, 979.508196700000, 881.147541000000, 367.131147500000]
        values = [0.466860146000000, 0.971605616000000, 1.90838497100000, 2.84092870000000,
                  3.94501529500000, 4.96368342600000, 5.81645619300000, 6.58557533900000, 7.35469448600000,
                  8.64020707500000, 9.84312495100000, 11.8225743200000, 13.3721076200000, 14.9219938800000,
                  16.4729390500000, 18.1103616000000, 19.7040160000000, 21.3417915100000, 22.2955133700000,
                  22.7321358500000, 22.8690877700000, 22.9608596800000, 23.0956937800000, 23.2340575700000,
                  23.3272413500000, 23.3770099600000, 23.5136089100000, 23.5623186100000, 23.7035061600000]
        values_new = range(1440)
        Charge_Prob_new2 = user_definedProb(Charge_Freq, values)
        arrivalTime = np.random.choice(values_new, nVech, p=list(Charge_Prob_new2))
        return arrivalTime/60

def user_definedProb(freq, values):
    total_freq = sum(freq)
    return [f/total_freq for f in freq]


import pulp as lp

def solve_milp(t, EEV, Emin, Emax, Pch_max, Pdis_max, base_Load, unmanaged_Load, n):
    # Define the MILP problem
    model = lp.LpProblem('EV_Optimization', lp.LpMinimize)

    # Define decision variables
    chargeprofiles = lp.LpVariable.dicts('chargeprofiles', ((i, t) for i in range(n) for t in range(24)), lowBound=0, upBound=Pch_max.max())
    dischargeprofiles = lp.LpVariable.dicts('dischargeprofiles', ((i, t) for i in range(n) for t in range(24)), lowBound=-Pdis_max.max(), upBound=0)
    total_load = lp.LpVariable.dicts('total_load', range(24), lowBound=0)
    max_load = lp.LpVariable('max_load', lowBound=0)

    # Objective function: Minimize the maximum load
    model += max_load

    # Constraints for maximum load
    for t in range(24):
        model += total_load[t] <= max_load

    # Calculate total load at each time interval
    for t in range(24):
        model += lp.lpSum([chargeprofiles[i, t] for i in range(n)]) + lp.lpSum([dischargeprofiles[i, t] for i in range(n)]) + base_Load[t] + unmanaged_Load[t] == total_load[t]

    # EV constraints
    for t in range(24):
        for i in range(n):
            model += chargeprofiles[i, t] <= Pch_max[t, i]
            model += dischargeprofiles[i, t] >= -Pdis_max[t, i]
            model += EEV[t, i] + chargeprofiles[i, t] * ηch - dischargeprofiles[i, t] / ηdis <= Emax[t, i]
            model += EEV[t, i] + chargeprofiles[i, t] * ηch - dischargeprofiles[i, t] / ηdis >= Emin[t, i]

    # Solve the model
    status = model.solve()
    print(f"Status: {lp.LpStatus[status]}")
    print(f"Max Load: {lp.value(max_load)}")

    # Extract the results
    charge_result = {k: v.varValue for k, v in chargeprofiles.items()}
    discharge_result = {k: v.varValue for k, v in dischargeprofiles.items()}
    total_load_result = {k: v.varValue for k, v in total_load.items()}

    return charge_result, discharge_result, total_load_result



import numpy as np

# Example input parameters
n = 10  # Number of EVs
useCase = 2  # Office use case
tarr = getArrivalTime(n, useCase)
tch = np.random.randint(0, 24, n)  # Charging start times
tdep = np.random.randint(0, 24, n)  # Departure times
Eini = np.random.uniform(0, 1, n)  # Initial battery energy

# Constants
Emin0 = 0.1
Emax0 = 1.0
Pch_max0 = 10  # kW
Pdis_max0 = 10  # kW
ηch = 0.9  # Charging efficiency
ηdis = 0.9  # Discharging efficiency

# Initialize output matrices
EEV = np.zeros((24, n))
Emin = np.zeros((24, n))
Emax = np.zeros((24, n))
Pch_max = np.zeros((24, n))
Pdis_max = np.zeros((24, n))

# Base load and unmanaged load for each hour
base_Load



import numpy as np

# Example input parameters
n = 10  # Number of EVs
useCase = 2  # Office use case
tarr = getArrivalTime(n, useCase)
tch = np.random.randint(0, 24, n)  # Charging start times
tdep = np.random.randint(0, 24, n)  # Departure times
Eini = np.random.uniform(0, 1, n)  # Initial battery energy

# Constants
Emin0 = 0.1
Emax0 = 1.0
Pch_max0 = 10  # kW
Pdis_max0 = 10  # kW
ηch = 0.9  # Charging efficiency
ηdis = 0.9  # Discharging efficiency

# Initialize output matrices
EEV = np.zeros((24, n))
Emin = np.zeros((24, n))
Emax = np.zeros((24, n))
Pch_max = np.zeros((24, n))
Pdis_max = np.zeros((24, n))

# Example base load and unmanaged load for each hour (you can replace these with actual data)
base_Load = np.random.uniform(5, 10, 24)  # kW
unmanaged_Load = np.random.uniform(2, 5, 24)  # kW

# Step 4: Continued - Dynamic MILP Trigger on EV Arrival

for t in range(24):
    for i in range(n):
        if t < tarr[i]:
            # EV has not arrived yet, initialize variables to 0
            EEV[t, i] = 0
            Emin[t, i] = 0
            Emax[t, i] = 0
            Pch_max[t, i] = 0
            Pdis_max[t, i] = 0
        elif t == tarr[i]:
            # EV has arrived, initialize initial conditions
            EEV[t, i] = Eini[i]
            Emin[t, i] = max(Emin0, Eini[i] - Pdis_max0 * ηdis * (t - tarr[i]))
            Emax[t, i] = min(Emax0, Eini[i] + Pch_max0 * ηch * (t - tarr[i]))
            Pch_max[t, i] = Pch_max0
            Pdis_max[t, i] = Pdis_max0
        else:
            # EV is already arrived, update conditions
            if t <= tch[i] and t > tarr[i]:
                EEV[t, i] = EEV[t-1, i] - Pdis_max0 * ηdis * (t - tarr[i])
                Emin[t, i] = max(Emin0, Eini[i] - Pdis_max0 * ηdis * (t - tarr[i]))
                Emax[t, i] = min(Emax0, Eini[i] + Pch_max0 * ηch * (t - tarr[i]))
                Pch_max[t, i] = Pch_max0
                Pdis_max[t, i] = Pdis_max0
            elif t > tch[i] and t <= tdep[i]:
                EEV[t, i] = EEV[t-1, i] - Pdis_max0 * ηdis * (t - tarr[i])
                Emin[t, i] = Emin0 + Pch_max0 * ηch * (t - tch[i])
                Emax[t, i] = Emax0
                Pch_max[t, i] = Pch_max0
                Pdis_max[t, i] = Pdis_max0
            elif t > tdep[i]:
                EEV[t, i] = 0
                Emin[t, i] = 0
                Emax[t, i] = 0
                Pch_max[t, i] = 0
                Pdis_max[t, i] = 0

            # Trigger MILP optimization when EV arrives or conditions change
            if t == tarr[i] or t == tch[i] or t == tdep[i]:
                # Solve MILP to get optimized profiles
                charge_result, discharge_result, total_load_result = solve_milp(t, EEV, Emin, Emax, Pch_max, Pdis_max, base_Load, unmanaged_Load, n)

                # Use charge_result and discharge_result as needed for control actions
                # Example: Set EV charging profiles based on charge_result
                print(f"Optimized Charging Profiles at t={t}:")
                print(charge_result)

                # Example: Set EV discharging profiles based on discharge_result
                print(f"Optimized Discharging Profiles at t={t}:")
                print(discharge_result)

                # Update EEV, Emin, Emax, Pch_max, Pdis_max based on optimization results
                for j in range(24):
                    EEV[j, i] = EEV[j, i] + charge_result[i, j] * ηch - discharge_result[i, j] / ηdis
                    Emin[j, i] = max(Emin0, EEV[j, i] - Pdis_max0 * ηdis * (j - tarr[i]))
                    Emax[j, i] = min(Emax0, EEV[j, i] + Pch_max0 * ηch * (j - tarr[i]))
                    Pch_max[j, i] = Pch_max0
                    Pdis_max[j, i] = Pdis_max0

# Step 5: Further actions or outputs can be added here as needed