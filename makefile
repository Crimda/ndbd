all:clean
clean:
	@echo "[Purging *.pyc files...]"
	find . -name "*.pyc" -delete
	@echo "[Cleanup complete.]"

