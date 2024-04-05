

# t = np.arange(0, DURATION, 1 / SAMPLE_RATE)
# signal = np.sin(1000 * (2 * np.pi) * t) + 0.3 * np.sin(5000 * (2 * np.pi) * t)
# SAMPLE_RATE = 40_000
data = data_test


# t = np.arange(0, len(data_wav) / SAMPLE_RATE,  1 / SAMPLE_RATE)
#signal = np.array(data, dtype=np.float64)

# signal = signal / 4095 * 2 - 1
#signal = np.interp(signal, (signal.min(), signal.max()), (-1, 1))

print(t)
print(signal)



print(fft_result)

# Определение индексов для диапазона частот от 100 Гц до 18000 Гц





plt.figure(figsize=(100, 60))
plt.plot(t, signal)
plt.show()