import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## Config setting
init_capital = 100
days = 100
simulations_times = 1000
outer_runs = 100 # 100 times independent simulations -> draw 100 lines 

def simulate_once(init_capital, days):
  #　Daily rate of return +1% or -1%
  daily_returns_list = np.where(np.random.rand(days) < 0.51, 0.01, -0.01)

  # Calculate daily asset changes
  asset_values = [init_capital]
  for ror in daily_returns_list:
          asset_values.append(asset_values[-1] * (1 + ror))

  return np.array(daily_returns_list), np.array(asset_values[1:]) # first day "init_capital" doesn't need return in asset_value

## Monte Carol simulation
daily_sharp_ratios = []
annual_sharp_ratios = []
for _ in range(simulations_times):
  daily_returns_list, asset_values = simulate_once(init_capital, days)
  mean_return = np.mean(daily_returns_list)
  std_return = np.std(daily_returns_list)
    
  if std_return > 0:
      annual_factor = np.sqrt(252) # suppose 252 trading days per year
      daily_sharp_ratios.append(mean_return / std_return)  # suppose "Rf" is 0
      annual_sharp_ratios.append((mean_return / std_return) * annual_factor)

## Result statistics
avg_sharp_ration = np.mean(daily_sharp_ratios)
avg_annual_sharp_ratio = np.mean(annual_sharp_ratios)
print(f"Average Sharpe Ratio after {simulations_times} simulations: {avg_sharp_ration:.4f}")
print(f"Average Annual Sharpe Ratio after {simulations_times} simulations: {avg_annual_sharp_ratio:.4f}")

df = pd.DataFrame({
    "Day": np.arange(1, days + 1),
    "Daily Return": daily_returns_list,
    "Asset Value": asset_values
})
print(df.head(100))

## Additional 100 simulations were performed for plotting.
asset_curves = []

for i in range(outer_runs):
    _, asset_values = simulate_once(init_capital, days)
    asset_curves.append(asset_values)
asset_curves = np.array(asset_curves)

# Find the highest and lowest final asset
final_values = asset_curves[:, -1]
max_idx = np.argmax(final_values)
min_idx = np.argmin(final_values)

# Calculate mean asset trajectory and Bollinger Bands(±1σ)
mean_curve = np.mean(asset_curves, axis=0)
std_curve = np.std(asset_curves, axis=0)
upper_bound = mean_curve + std_curve
lower_bound = mean_curve - std_curve

## Plotting
plt.figure(figsize=(10, 6))

for i in range(outer_runs):
  if i == max_idx:
    plt.plot(range(1, days + 1), asset_curves[i], color='red', linewidth=2, label='Highest Final Asset')
  elif i == min_idx:
    plt.plot(range(1, days + 1), asset_curves[i], color='blue', linewidth=2, label='Lowest Final Asset')
  else:
     plt.plot(range(1, days + 1), asset_curves[i], color='gray', alpha=0.3)

# mean asset trajectory
plt.plot(range(1, days + 1), mean_curve, color='black', linewidth=2.5, label='Mean Asset Curve')

# ±1σ interval
plt.fill_between(range(1, days + 1), lower_bound, upper_bound, color='orange', alpha=0.2, label='±1σ Range')

plt.plot(df["Day"], df["Asset Value"])
plt.title("Asset Value Over {days} Days (100 Simulations)")
plt.xlabel("Day")
plt.ylabel("Asset Value ($)")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print(f"Highest final asset value: {final_values[max_idx]:.2f}")
print(f"Lowest final asset value:  {final_values[min_idx]:.2f}")

