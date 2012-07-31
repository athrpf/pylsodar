
all: _lsodar.so

test: _lsodar.so
	python test_lsodar.py

_lsodar.so: lsodar.pyf opkdmain.f opkda1.f opkda2.f
	f2py -c lsodar.pyf opkdmain.f opkda1.f opkda2.f

