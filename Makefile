

all: lsodar.pyf opkdmain.f opkda1.f opkda2.f
	f2py -c lsodar.pyf opkdmain.f opkda1.f opkda2.f
