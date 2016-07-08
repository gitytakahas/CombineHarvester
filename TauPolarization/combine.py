import math

#cent = 2.
#err = 1.

cent = 10.
err = 3.

#cent = 1.
#err = 0.5

print "prior = 0 +/- 1"
print "free fit = ", cent, "+/-", err
print "significance of the free fit = ", cent/err

comb_cent = cent/(err*err+1)
comb_err = math.sqrt(err*err/(err*err+1))

print "combination (pull) =>", comb_cent, "+/-", comb_err

comb_sig = comb_cent/(comb_err*math.sqrt(1-comb_err*comb_err))

print "calculated significance from pull = ", comb_sig
