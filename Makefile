build:
	rm -rf AttributeTransfer && \
	rm -f AttributeTransfer.zip && \
	mkdir AttributeTransfer && \
	find . ! -path "*/\.*" ! -path "./AttributeTransfer*" ! -path "." ! -path "*.pyc" -exec cp -r {} AttributeTransfer \; && \
	rm -f ./AttributeTransfer/tests/*.pyc && \
	zip -r AttributeTransfer.zip ./AttributeTransfer && \
	rm -rf AttributeTransfer
