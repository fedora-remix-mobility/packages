srpm:
	sed -i -e "s/%autorelease/$(shell date +%s)/" *.spec
	dnf install -y rpkg rpmdevtools
	spectool -g *.spec
	rpkg srpm --outdir=.
	mv *.src.rpm $(outdir)/
