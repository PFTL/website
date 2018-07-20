import random

observations = ['Real', 'Fake']
flowers = ['Iris setosa', 'Iris virginica', 'Iris versicolor']

with open('DA_data.dat', 'w') as f:
    for _ in range(20):
        observation = random.choice(observations)
        flower = random.choice(flowers)
        f.write('{} {}\n'.format(observation, flower))
