# Імпортуємо необхідні бібліотеки
import numpy as np  
import matplotlib.pyplot as plt

# 1. Генеруємо випадкові дані навколо прямої y = 2x + 1
true_k = 2 # Задаємо справжній нахил прямої
true_b = 1 # Задаємо справжній зсув прямої 

num_points = 50 # Кількість точок для генерації
x = np.random.uniform(0, 10, size=num_points) # Генеруємо випадкові x з рівномірним розподілом
y = true_k*x + true_b + np.random.normal(0, 3, size=num_points) # Обчислюємо y з додаванням шуму

# 2. Функція МНК 
def least_squares(x, y):

    # Обчислюємо середні 
    x_mean = np.mean(x)  
    y_mean = np.mean(y)
    
    # За формулою МНК
    num = np.sum((x - x_mean) * (y - y_mean))
    den = np.sum((x - x_mean)**2)

    # Обчислюємо параметри    
    k = num / den
    b = y_mean - k*x_mean

    return k, b

# 3. Порівнюємо з np.polyfit
k_ls, b_ls = least_squares(x, y) 
k_np, b_np = np.polyfit(x, y, 1)

print(f'МНК: k={k_ls:.3f}, b={b_ls:.3f}')
print(f'NumPy: k={k_np:.3f}, b={b_np:.3f}')
print(f'Істинні: k={true_k:.3f}, b={true_b:.3f}')

# 4. Будуємо графіки
plt.scatter(x, y) # Розсіяний графік даних

plt.plot(x, true_k*x + true_b, c='black') # Істинна пряма  

y_pred_ls = k_ls*x + b_ls 
plt.plot(x, y_pred_ls, c='blue', label='МНК') # Пряма МНК

y_pred_np = k_np*x + b_np
plt.plot(x, y_pred_np, c='red', label='NumPy') # Пряма NumPy

plt.legend()
plt.xlabel('x')  
plt.ylabel('y')
plt.title('Порівняння МНК та NumPy')
plt.show()


# 1. Градієнтний спуск
def grad_descent(x, y, learning_rate=0.1, n_iter=100):
    
    b = 0  
    k = 0
    cost_history = []
    
    for i in range(n_iter):
        
        # Обчислюємо прогноз
        y_pred = k*x + b  
        # Обчислюємо функцію втрат    
        cost = np.mean((y - y_pred)**2)  
        # Зберігаємо функцію втрат
        cost_history.append(cost)
        
        # Обчислюємо градієнти
        kb_grad = -(2/num_points) * np.sum((y - y_pred) * x)  
        b_grad = -(2/num_points) * np.sum(y - y_pred)
        
        # Оновлюємо ваги моделі
        k = k - learning_rate * kb_grad   
        b = b - learning_rate * b_grad
        
    return k, b, cost_history

k_gd, b_gd, costs = grad_descent(x, y)
print(f'Градієнтний спуск: k={k_gd:.3f}, b={b_gd:.3f}')

# 2. Додавання на графік
y_pred_gd = k_gd*x + b_gd 
plt.plot(x, y_pred_gd, c='green', label='Градієнтний спуск')

# 3. Графік похибки
plt.figure()
plt.plot(costs)
plt.ylabel('Похибка')  
plt.xlabel('Ітерація')

plt.legend()
plt.show()