# Change this to the version you use :)
BINPATH=/usr/bin
CFGPATH=/etc/
DOCPATH=/usr/doc
all:
	@echo "Please specify operation"
	@echo "========================"
	@echo "Available operations:"
	@echo ""
	@echo "Note: for the following 3 rules, you can also pre-append \"full-\" to also include bundled tools, or append \"-tools\" to only install the bundled tools."
	@echo
	@echo "install		-	install server."
	@echo "uninstall	-	uninstall server."
	@echo "update		-	Helper, executes uninstall then install rules."
	@echo "PURGE		-	purge all git info and this makefile (ONE WAY OPERATION)."
	@echo "clean		-	remove all *pyc files and the un-needed wst directory."
	@echo "======================="
	@echo "Remember, for de/installation, you must use sudo!"
	@echo ""

install:
	@echo "Not yet implemented"

full-install:
	@echo "Not yet implemented"

install-tools:
	@echo "Not yet implemented"

uninstall:
	@echo "Not yet implemented"

full-uninstall:
	@echo "Not yet implemented"

uninstall-tools:
	@echo "Not yet implemented"

update:
	@echo "Not yet implemented"

full-update:
	@echo "Not yet implemented"

update-tools:
	@echo "Not yet implemented"

PURGE:
	rm -rf .git*
	rm makefile

clean:
	@echo "[Purging *.pyc files...]"
	find . -name "*.pyc" -delete
	@echo "[Cleanup complete.]"
