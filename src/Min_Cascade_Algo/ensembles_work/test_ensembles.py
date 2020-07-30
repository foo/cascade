from ensembles_work import ensembles

k = 10
l = 2
percentage = 10

e = ensembles.Ensembles(k, l, percentage)
c1 = e.list_ensembles[0]
c2 = e.list_ensembles[1]

print(c1, c2)

partition_number = e.find_prime_partition_number(c1, c2)
print("prime partition number: ", partition_number)