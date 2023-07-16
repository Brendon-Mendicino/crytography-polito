from Crypto.Util.number import long_to_bytes

n = 80874201765154818839855154192074564845947935090732132114512998680006465697428706028107212101624175109119715651660627873351375111994696452501912697968038549202222203735417132150705652868244910670206026911255317593082755496497124976433315702174116991149774757597676214004436682022708978322786435515230194378709

c = 36988748523145895012935109133829495333903772995218396754301218746268506086806980023815197713075232396341180777688664098368951689232915516431991224311490005139853383886692715006589554332344335391980870775784994494698509478569459752335447593578160974888437129403015438850328650209840545939867557758411669066787

c_inverse = pow(c, -1, n)
print(c_inverse)

# = c_inverse ^ d mod n
m_inverse = 388061399801285851919593542929760054985712886987094379740956040557862559104225806798979403084002061128298387675489458283785190656657205901127126834707921432589676921708784314719157579597502180744319901504105135732580290398597679571646623695091560414422277777948036095754815756116575725937626837942015426897

m = pow(m_inverse, -1, n)
print(long_to_bytes(m))