import numpy

def nn(m1, m2, w1, w2, b):
    x = m1 * w1 + m2 * w2 + b
    return 1 / (1 + numpy.exp(-x))


# w1 = numpy.random.randn()
# w2 = numpy.random.randn()
# b = numpy.random.randn()
w1 = 37.19669196493046
w2 = 18.446618365111977
b = -134.50328937729142

phrases = ['seems like it`s', 'I guess', 'I think', 'possibly', 'looks like', 'guessing...']
data = [[3, 1.5, 1], [2, 1, 0], [4, 1.5, 1], [3, 1, 0], [3.5, 0.5, 1], [2, 0.5, 0], [5.5, 1, 1], [1, 1, 0]]
rand_data = data[numpy.random.randint(len(data))]

m1 = rand_data[0]
m2 = rand_data[1]

prediction = nn(m1, m2, w1, w2, b)
prediction_text = ['blue', 'red'][int(numpy.round(prediction))]

phrase = numpy.random.choice(phrases) + ' ' + prediction_text
print(phrase)

print('It`s really ' + ["blue", 'red'][rand_data[2]])
