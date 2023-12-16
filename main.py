import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons

# Початкові значення параметрів
init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.5
init_noise_covariance = 0.5
init_show_noise = True

# Функція, яка генерує графік
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, t):
    clean_signal = amplitude * np.sin(frequency * t + phase)
    noise = np.random.normal(noise_mean, noise_covariance, size=len(t))
    signal_with_noise = clean_signal + noise if show_noise else clean_signal
    return signal_with_noise

t = np.linspace(0, 2*np.pi, 1000)

# Створення графічного вікна та графіку
fig, ax = plt.subplots()
line, = ax.plot(t, harmonic_with_noise(init_amplitude, init_frequency, init_phase, init_noise_mean, init_noise_covariance, init_show_noise, t), lw=2)
ax.set_xlabel('Time')

# Налаштування місця для слайдерів та елементів інтерфейсу
fig.subplots_adjust(left=0.25, bottom=0.45)

# Створення слайдерів для амплітуди, частоти, шуму та чекбоксу для відображення шуму
ax_amp = fig.add_axes([0.25, 0.3, 0.65, 0.03])
amp_slider = Slider(
    ax=ax_amp,
    label='Amplitude',
    valmin=0.1,
    valmax=2.0,
    valinit=init_amplitude,
)

ax_freq = fig.add_axes([0.25, 0.25, 0.65, 0.03])
freq_slider = Slider(
    ax=ax_freq,
    label='Frequency',
    valmin=0.1,
    valmax=5.0,
    valinit=init_frequency,
)

ax_phase = fig.add_axes([0.25, 0.2, 0.65, 0.03])
phase_slider = Slider(
    ax=ax_phase,
    label='Phase',
    valmin=0.0,
    valmax=2*np.pi,
    valinit=init_phase,
)

ax_noise_mean = fig.add_axes([0.25, 0.15, 0.65, 0.03])
noise_mean_slider = Slider(
    ax=ax_noise_mean,
    label='Noise Mean',
    valmin=0.0,
    valmax=1.0,
    valinit=init_noise_mean,
)

ax_noise_cov = fig.add_axes([0.25, 0.1, 0.65, 0.03])
noise_cov_slider = Slider(
    ax=ax_noise_cov,
    label='Noise Covariance',
    valmin=0.0,
    valmax=1.0,
    valinit=init_noise_covariance,
)

# Чекбокс для регулювання шуму (вмикати / вимикати)
ax_checkbox = fig.add_axes([0.03, 0.55, 0.12, 0.05])
checkbox = CheckButtons(ax_checkbox, ['Show Noise'], [init_show_noise])

# Оновлення графіку при зміні параметрів
def update(val):
    amplitude = amp_slider.val
    frequency = freq_slider.val
    phase = phase_slider.val
    noise_mean = noise_mean_slider.val
    noise_covariance = noise_cov_slider.val
    show_noise = checkbox.get_status()[0]
    
    line.set_ydata(harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, t))
    fig.canvas.draw_idle()

# Реєстрація функції для слайдерів та чекбоксу
amp_slider.on_changed(update)
freq_slider.on_changed(update)
phase_slider.on_changed(update)
noise_mean_slider.on_changed(update)
noise_cov_slider.on_changed(update)
checkbox.on_clicked(update)

# Функція для скидання параметрів до початкових значень
def reset(event):
    amp_slider.reset()
    freq_slider.reset()
    phase_slider.reset()
    noise_mean_slider.reset()
    noise_cov_slider.reset()
    update(None)

# Кнопка для скидання параметрів
resetax = fig.add_axes([0.03, 0.45, 0.12, 0.05])
reset_button = Button(resetax, 'Reset')
reset_button.on_clicked(reset)

plt.show()
